from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from logger_config import logger
from evidence_logic import evidence_mapper
from deep_translator import GoogleTranslator

# Specialist Imports
from urdu_voice import generate_urdu_response
from english_voice import generate_english_response

# ─── LLM: gemma4:26b hosted on remote server ───────────────────────────────
REMOTE_LLM_BASE = "http://203.124.40.57:11434"
LLM_MODEL = "gemma4:26b"

class AgentState(TypedDict):
    query: str
    raw_query: str          # original user query (before any rewriting)
    english_query: str      # query translated to English for vector retrieval
    category: str
    context: str
    translated_context: str
    response: str
    language: str
    evidence: List[str]

def create_dastoor_graph(vector_db, legal_tools):
    # timeout=120 ensures the LLM never hangs indefinitely
    llm = OllamaLLM(
        model=LLM_MODEL,
        base_url=REMOTE_LLM_BASE,
        temperature=0,
        timeout=120,
        client_kwargs={'timeout': 120.0}
    )

    # ── NODE 1: Language Classifier + Query Pre-Translator ──────────────────
    def classifier_node(state: AgentState):
        is_urdu = any('\u0600' <= c <= '\u06FF' for c in state['query'])
        detected_lang = "urdu" if is_urdu else "english"
        logger.info(f"[NODE] Classifier: Detected '{detected_lang}' | Category: {state['category']}")

        if is_urdu:
            try:
                english_query = GoogleTranslator(source='ur', target='en').translate(state['query'])
                logger.info(f"[NODE] Classifier: Translated query for retrieval-> '{english_query}'")
            except Exception as trans_err:
                logger.warning(f"[NODE] Classifier: Translation failed ({trans_err}), using original query.")
                english_query = state['query']
        else:
            english_query = state['query']

        return {
            # Initialize ALL state fields with safe defaults to prevent KeyErrors
            "query":              state['query'],
            "raw_query":         state['query'],       # original query preserved here
            "english_query":     english_query,         # English version for retrieval
            "category":          state.get('category', ''),
            "language":          detected_lang,
            "context":           state.get('context', ''),
            "translated_context": state.get('translated_context', ''),
            "response":          state.get('response', ''),
            "evidence":          state.get('evidence', []),
        }

    # ── NODE 2: Query Rewriter ───────────────────────────────────────────────
    def query_rewriter_node(state: AgentState):
        """
        Rewrites the English version of the query into a formal Pakistani legal
        search query. Always operates in English so MPNet retrieval works correctly.
        """
        logger.info(f"[NODE] Rewriter: Rewriting english_query for better retrieval...")
        prompt = (
            f"Rewrite the following user query as a semantic legal search phrase in English. "
            f"Legal domain: {state['category']}. "
            f"User query: {state['english_query']}\n\n"
            f"Rules:\n"
            f"- Output ONLY the rewritten search phrase in English, nothing else.\n"
            f"- Describe the LEGAL CONCEPT or SITUATION the user is asking about (e.g. 'online harassment punishment', 'wrongful termination compensation'). \n"
            f"- Do NOT include any specific section numbers, article numbers, or clause references — these will be found by the database.\n"
            f"- You may include the Act name ONLY if it is well-known and directly relevant.\n"
            f"- Keep it to 1-2 sentences maximum."
        )
        rewritten = llm.invoke(prompt).strip()
        logger.info(f"[NODE] Rewriter: '{state['english_query']}'-> '{rewritten}'")
        return {**state, "english_query": rewritten}

    # ── NODE 3: Retriever with Relevance Filtering ───────────────────────────
    def retriever_node(state: AgentState):
        # Always use the English query for vector search (MPNet is English-only)
        retrieval_query = state.get('english_query') or state['query']
        logger.info(f"[NODE] Retriever: Fetching law for category='{state['category']}' | query='{retrieval_query[:60]}...'")

        MIN_SCORE = 0.20  # slightly lower = more section coverage
        scored_results = []

        try:
            # ── Stage 1: Category-filtered search ───────────────────────────
            scored_results = vector_db.similarity_search_with_relevance_scores(
                retrieval_query,
                k=20,                          # increased from 8 → 20
                filter={"category": state['category']}
            )
            logger.info(f"[NODE] Retriever: Stage-1 filter returned {len(scored_results)} chunks.")

            # ── Stage 2: Unfiltered fallback if filter matched nothing ───────
            if len(scored_results) == 0:
                logger.warning(f"[NODE] Retriever: Category '{state['category']}' -> unfiltered fallback.")
                scored_results = vector_db.similarity_search_with_relevance_scores(
                    retrieval_query, k=15      # increased from 8 → 15
                )

        except Exception as retrieval_err:
            logger.error(f"[NODE] Retriever: scored search failed ({retrieval_err}) — plain fallback.")
            try:
                plain_docs = vector_db.similarity_search(retrieval_query, k=8)  # increased from 5 → 8
                scored_results = [(doc, 1.0) for doc in plain_docs]
            except Exception as plain_err:
                logger.error(f"[NODE] Retriever: plain search also failed ({plain_err}).")
                scored_results = []

        # ── Stage 3: Score threshold filter ─────────────────────────────────
        filtered = [(doc, score) for doc, score in scored_results if score >= MIN_SCORE]
        if not filtered:
            logger.warning("[NODE] Retriever: All scores below threshold — using top-5 fallback.")
            filtered = scored_results[:5]

        # Sort by score descending, keep top-15 for richer section coverage
        filtered.sort(key=lambda x: x[1], reverse=True)
        top_docs = filtered[:15]              # increased from 10 → 15

        # Build rich context with source + score info for the LLM
        context_parts = []
        for doc, score in top_docs:
            source = doc.metadata.get('source', 'Pakistani Law')
            cat = doc.metadata.get('category', state['category'])
            context_parts.append(
                f"[SOURCE: {source} | Category: {cat} | Relevance: {score:.2f}]\n"
                f"{doc.page_content}"
            )
        context = "\n\n---\n\n".join(context_parts)

        evidence = evidence_mapper.get_evidence_checklist(state['category'])
        logger.info(f"[NODE] Retriever: Retrieved {len(top_docs)} chunks (of {len(scored_results)} fetched).")
        return {**state, "context": context, "evidence": evidence}

    # ── NODE 4: Urdu Context Prep (only reached by Urdu queries) ─────────────
    # English queries are routed DIRECTLY from retriever → reasoner via the
    # conditional edge below and NEVER enter this node.
    # For Urdu queries: context stays as English (the LLM is capable of
    # reasoning over English law and answering in Urdu).
    def translator_node(state: AgentState):
        logger.info("[NODE] Translator: Urdu path — preparing context for Urdu specialist.")
        # Pass English context through; urdu_voice prompt handles Urdu output.
        return {**state, "translated_context": state['context']}

    # ── ROUTING 1: after classifier, English skips rewriter → retriever directly
    # Urdu needs the rewriter to convert translated text into formal legal English.
    # English is already well-formed; skipping saves one full LLM round-trip.
    def route_after_classifier(state: AgentState) -> str:
        if state.get('language') == 'urdu':
            return 'query_rewriter'
        return 'retriever'  # English: skip rewriter, go straight to retrieval

    # ── ROUTING 2: after retriever, English skips translator entirely ──────────
    def route_after_retriever(state: AgentState) -> str:
        if state.get('language') == 'urdu':
            return 'translator'
        return 'reasoner'  # English goes straight to reasoner — no extra node
    # ── NODE 5: Reasoner — routes to language-specific specialist ────────────
    def reasoner_node(state: AgentState):
        logger.info(f"[NODE] Reasoner: Calling {state['language'].upper()} specialist...")

        # Use the ORIGINAL user query for the response, not the rewritten one
        original_query = state.get('raw_query', state['query'])

        if state['language'] == "urdu":
            response = generate_urdu_response(
                original_query,
                state['translated_context'],
                state['category'],
                state['evidence']
            )
        else:
            response = generate_english_response(
                original_query,
                state['context'],
                state['category'],
                state['evidence']
            )

        return {**state, "response": response}

    # ── BUILD WORKFLOW ───────────────────────────────────────────────────────
    workflow = StateGraph(AgentState)
    workflow.add_node("classifier",     classifier_node)
    workflow.add_node("query_rewriter", query_rewriter_node)  # Urdu path only
    workflow.add_node("retriever",      retriever_node)
    workflow.add_node("translator",     translator_node)       # Urdu path only
    workflow.add_node("reasoner",       reasoner_node)

    workflow.set_entry_point("classifier")

    # English & Urdu → retriever directly (No rewriter step to save time)
    workflow.add_edge("classifier", "retriever")

    # English → reasoner directly; Urdu → translator → reasoner
    workflow.add_conditional_edges(
        "retriever",
        route_after_retriever,
        {"translator": "translator", "reasoner": "reasoner"}
    )
    workflow.add_edge("translator",     "reasoner")
    workflow.add_edge("reasoner",       END)

    return workflow.compile()
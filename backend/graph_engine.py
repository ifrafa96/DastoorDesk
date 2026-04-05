from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from logger_config import logger
from evidence_logic import evidence_mapper

# Specialist Imports
from urdu_voice import generate_urdu_response
from english_voice import generate_english_response

# ─── LLM: gemma4:26b hosted on remote server ───────────────────────────────
REMOTE_LLM_BASE = "http://203.124.40.57:11434"
LLM_MODEL = "gemma4:26b"

class AgentState(TypedDict):
    query: str
    raw_query: str          # original user query (before rewriting)
    category: str
    context: str
    translated_context: str
    response: str
    language: str
    evidence: List[str]

def create_dastoor_graph(vector_db, legal_tools):
    llm = OllamaLLM(model=LLM_MODEL, base_url=REMOTE_LLM_BASE, temperature=0)

    # ── NODE 1: Language Classifier ─────────────────────────────────────────
    def classifier_node(state: AgentState):
        is_urdu = any('\u0600' <= c <= '\u06FF' for c in state['query'])
        detected_lang = "urdu" if is_urdu else "english"
        logger.info(f"[NODE] Classifier: Detected '{detected_lang}' | Category: {state['category']}")
        return {
            **state,
            "language": detected_lang,
            "raw_query": state['query'],   # preserve original before rewriting
        }

    # ── NODE 2: Query Rewriter ───────────────────────────────────────────────
    def query_rewriter_node(state: AgentState):
        """
        Rewrites the user's casual/vague question into a formal Pakistani legal
        search query so vector retrieval matches actual law text much better.
        """
        logger.info(f"[NODE] Rewriter: Rewriting query for better retrieval...")
        prompt = (
            f"Rewrite the following user query as a precise Pakistani legal search query. "
            f"Legal domain: {state['category']}. "
            f"User language: {state['language']}. "
            f"User query: {state['query']}\n\n"
            f"Rules:\n"
            f"- Output ONLY the rewritten query, nothing else.\n"
            f"- Keep it in the SAME language as the user query.\n"
            f"- Include relevant Pakistani act names, section keywords if known.\n"
            f"- Make it concise and specific (1-2 sentences max)."
        )
        rewritten = llm.invoke(prompt).strip()
        logger.info(f"[NODE] Rewriter: '{state['query']}' → '{rewritten}'")
        return {**state, "query": rewritten}

    # ── NODE 3: Retriever with Relevance Filtering ───────────────────────────
    def retriever_node(state: AgentState):
        logger.info(f"[NODE] Retriever: Fetching law for category='{state['category']}'")

        MIN_SCORE = 0.25
        scored_results = []

        try:
            # ── Stage 1: Category-filtered search ───────────────────────────
            scored_results = vector_db.similarity_search_with_relevance_scores(
                state['query'],
                k=8,
                filter={"category": state['category']}
            )
            logger.info(f"[NODE] Retriever: Stage-1 filter returned {len(scored_results)} chunks.")

            # ── Stage 2: Unfiltered fallback if filter matched nothing ───────
            if len(scored_results) == 0:
                logger.warning(f"[NODE] Retriever: Category '{state['category']}' -> unfiltered fallback.")
                scored_results = vector_db.similarity_search_with_relevance_scores(
                    state['query'], k=8
                )

        except Exception as retrieval_err:
            logger.error(f"[NODE] Retriever: scored search failed ({retrieval_err}) — plain fallback.")
            try:
                plain_docs = vector_db.similarity_search(state['query'], k=5)
                scored_results = [(doc, 1.0) for doc in plain_docs]
            except Exception as plain_err:
                logger.error(f"[NODE] Retriever: plain search also failed ({plain_err}).")
                scored_results = []

        # ── Stage 3: Score threshold filter ─────────────────────────────────
        filtered = [(doc, score) for doc, score in scored_results if score >= MIN_SCORE]
        if not filtered:
            logger.warning("[NODE] Retriever: All scores below threshold — using top-3 fallback.")
            filtered = scored_results[:3]

        # Sort by score descending, keep top-5
        filtered.sort(key=lambda x: x[1], reverse=True)
        top_docs = filtered[:5]

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

    # ── NODE 4: Translator (English context → Urdu for Urdu queries) ─────────
    def translator_node(state: AgentState):
        if state['language'] == "english":
            return {**state, "translated_context": state['context']}

        logger.info("[NODE] Translator: Translating English legal context → Urdu...")
        prompt = (
            f"Translate the following Pakistani legal clauses into professional Urdu script (اردو). "
            f"Preserve all Act names, Section numbers, and Article references in their original form.\n\n"
            f"{state['context']}"
        )
        translated = llm.invoke(prompt)
        return {**state, "translated_context": translated}

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
    workflow.add_node("query_rewriter", query_rewriter_node)
    workflow.add_node("retriever",      retriever_node)
    workflow.add_node("translator",     translator_node)
    workflow.add_node("reasoner",       reasoner_node)

    workflow.set_entry_point("classifier")
    workflow.add_edge("classifier",     "query_rewriter")
    workflow.add_edge("query_rewriter", "retriever")
    workflow.add_edge("retriever",      "translator")
    workflow.add_edge("translator",     "reasoner")
    workflow.add_edge("reasoner",       END)

    return workflow.compile()
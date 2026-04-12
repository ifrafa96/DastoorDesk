from langchain_ollama import OllamaLLM

# ─── Remote high-quality model ───────────────────────────────────────────────
llm = OllamaLLM(
    model="gemma4:26b",
    base_url="http://203.124.40.57:11434",
    temperature=0,
    timeout=120,  # prevent indefinite hang on slow remote server
    client_kwargs={'timeout': 120.0}
)

def generate_english_response(query, context, category, evidence):
    legal_focus = ""
    if "cybercrime" in category.lower():
        legal_focus = "Focus on PECA 2016 and related cybercrime legislation."
    elif "property" in category.lower():
        legal_focus = "Focus on Transfer of Property Act 1882 and Illegal Dispossession Act 2005."
    elif "family" in category.lower():
        legal_focus = "Focus on Muslim Family Laws Ordinance 1961 and Family Courts Act 1964."
    elif "labour" in category.lower():
        legal_focus = "Focus on Industrial Relations Act 2012 and EOBI Act 1976."
    elif "criminal" in category.lower():
        legal_focus = "Focus on Pakistan Penal Code 1860 and Code of Criminal Procedure 1898."
    elif "constitutional" in category.lower():
        legal_focus = "Focus on Constitution of Pakistan 1973, Fundamental Rights chapters."

    evidence_text = "\n".join(f"- {item}" for item in evidence)

    prompt = f"""You are Dastoor Desk — a strict Pakistani legal assistant. You ONLY handle Pakistani law.
The user asked a query in English. You MUST respond ONLY in English.

━━━ GLOBAL RULES (apply to ALL sections) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. PAKISTAN ONLY: You are restricted exclusively to Pakistani law. Never reference Indian IPC, UK law, US law, or any non-Pakistani legislation.
2. NO HALLUCINATION & VERBATIM NUMBERS: Never invent Act names, Section numbers, or Article references. Section numbers must be copied VERBATIM from the context.
3. ACCURACY & COMPLETENESS: You must be comprehensive. Identify and include ALL applicable sections of Pakistani law from the context (e.g., PPC, CPC, CrPC). You MUST extract multiple relevant sections (aim for 3 to 5 sections) to provide 100% complete legal coverage. Do NOT stop at just 1 or 2 sections if more apply.
4. SIMPLE LANGUAGE: Use clear, simple language so a common person can understand.
5. LEGAL FOCUS: {legal_focus}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RETRIEVED PAKISTANI LAW CONTEXT:
{context}

USER QUERY: {query}

━━━ REQUIRED RESPONSE STRUCTURE (Strictly follow this structure) ━━━━━━━━━━━━━━

### Legal Explanation
[Briefly and accurately explain the legal situation and facts under Pakistani law in English.]

### Applicable Laws
[RULES — TWO-STAGE PROCESS:
STAGE 1 (Relevance Test): Read EACH and EVERY part of the context thoroughly to hunt for applicable laws. Find ALL sections that relate to the user's question: '{query}'. You MUST find and extract multiple highly relevant sections (at least 2, up to 5) from the context to ensure a comprehensive answer out of the provided knowledge. Do not be lazy.
STAGE 2 (Verbatim Extraction): List ALL the sections you found in Stage 1. You MUST copy the Section number, Article number, and Act name VERBATIM from the context.
- If no directly relevant law is found in the context, write: "No matching Pakistani law found in the current database for this query."
]
[List ALL applicable statutes. For each statute, explicitly list ALL the specific section numbers found (2 to 5 sections if available) with short, accurate explanations in English.]

### What You Should Do
[Practical, real-world steps to take (e.g., FIR, lawyer, relevant Pakistani institutions like FIA, NADRA, Courts). Incorporate these evidence items:
{evidence_text}]
"""
    return llm.invoke(prompt)
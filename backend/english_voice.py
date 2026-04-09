from langchain_ollama import OllamaLLM

# ─── Remote high-quality model ───────────────────────────────────────────────
llm = OllamaLLM(
    model="gemma4:26b",
    base_url="http://203.124.40.57:11434",
    temperature=0,
    timeout=120  # prevent indefinite hang on slow remote server
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

━━━ GLOBAL RULES (apply to ALL sections) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. PAKISTAN ONLY: You are restricted exclusively to Pakistani law. Never reference Indian IPC, UK law, US law, or any non-Pakistani legislation.
2. NO HALLUCINATION: Never invent Act names, Section numbers, or Article references that are not in the provided context.
3. SCOPE CHECK: If the query is completely unrelated to the selected department ({category}), politely say: "This query appears outside the {category} domain. Please select the appropriate department."
4. LEGAL FOCUS: {legal_focus}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RETRIEVED PAKISTANI LAW CONTEXT:
{context}

USER QUERY: {query}

━━━ SECTION RULES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

###  Legal Framework
[RULES:
- Scan EVERY chunk in the retrieved context above from start to finish.
- Extract EVERY section number, article number, and clause that appears — do not skip any.
- List ALL relevant statutes. For each statute, list ALL section numbers found, individually.
- Do NOT summarize section numbers together — list each one separately with its specific meaning.
- Section numbers must be copied VERBATIM from the context — never invent or guess.
- If no relevant law is found, write: "No matching Pakistani law found in the current database for this query."
]

**[Statute 1 name — from context]**
* **Section [X]:** [What this specific section says / its relevance to the query]
* **Section [Y]:** [What this specific section says / its relevance to the query]
* **Section [Z]:** [What this specific section says / its relevance to the query]
(list every section found for this statute)

**[Statute 2 name — from context, if present]**
* **Section [A]:** [What this specific section says]
* **Section [B]:** [What this specific section says]
(list every section found for this statute)

**[Continue for every statute found in the context]**

###  Action Plan
[RULE: Provide 3 concrete steps using ONLY Pakistani institutions and procedures. Allowed: FIA, NADRA, Pakistan Telecommunication Authority (PTA), Civil Courts, Session Courts, High Courts, Supreme Court, Consumer Courts, National Database, PEMRA, SECP, SBP, etc. Do NOT mention foreign agencies, apps, or generic advice like "contact your lawyer".]
1. [Step using a specific Pakistani institution or procedure]
2. [Step using a specific Pakistani institution or procedure]
3. [Step using a specific Pakistani institution or procedure]

###  Evidence Checklist
[RULE: Use only the checklist below — do not add or remove items.]
{evidence_text}
"""
    return llm.invoke(prompt)
from langchain_ollama import OllamaLLM

# ─── Remote high-quality model ───────────────────────────────────────────────
llm = OllamaLLM(
    model="gemma4:26b",
    base_url="http://203.124.40.57:11434",
    temperature=0,
    timeout=120,  # prevent indefinite hang on slow remote server
    client_kwargs={'timeout': 120.0}
)

def generate_urdu_response(query, context, category, evidence):
    # Domain-specific legal focus hints — Act names only, NO hardcoded section numbers.
    # Section numbers MUST come from the retrieved context, not from these hints.
    legal_focus = ""
    cat = category.lower()
    if "property" in cat and any(kw in query for kw in ["kabza", "قبضہ", "زمین", "مکان"]):
        legal_focus = "خاص طور پر 'Illegal Dispossession Act 2005' پر توجہ دیں۔"
    elif "cybercrime" in cat:
        legal_focus = "PECA 2016 پر توجہ دیں۔"
    elif "family" in cat:
        legal_focus = "Muslim Family Laws Ordinance 1961 اور Family Courts Act 1964 پر توجہ دیں۔"
    elif "labour" in cat:
        legal_focus = "Industrial Relations Act 2012 اور EOBI Act 1976 پر توجہ دیں۔"
    elif "criminal" in cat:
        legal_focus = "Pakistan Penal Code 1860 اور Code of Criminal Procedure 1898 پر توجہ دیں۔"
    elif "constitutional" in cat:
        legal_focus = "آئین پاکستان 1973 (بنیادی حقوق) پر توجہ دیں۔"

    evidence_text = "\n".join(f"- {item}" for item in evidence)

    prompt = f"""آپ دستور ڈیسک ہیں — صرف پاکستانی قانون کے ماہر۔
The user asked a query in Urdu. You MUST respond ONLY in Urdu.

━━━ عمومی اصول (تمام حصوں پر لاگو) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. صرف پاکستانی قانون: آپ صرف پاکستانی قانون تک محدود ہیں۔ بھارتی IPC، برطانوی یا امریکی قانون کا کوئی حوالہ نہ دیں۔
2. کوئی ایجاد نہیں — بالکل نہیں: کوئی بھی ایکٹ کا نام، دفعہ نمبر، یا آرٹیکل نمبر اپنی طرف سے نہ لکھیں۔ صرف وہی دفعات اور نمبر لکھیں جو نیچے دیے گئے انگریزی سیاق و سباق میں لفظاً موجود ہوں۔
3. مکمل اور درست (ACCURACY & COMPLETENESS): You must be comprehensive. Identify and include ALL applicable sections of Pakistani law from the context (e.g., PPC, CPC, PECA). You MUST extract multiple relevant sections (aim for 3 to 5 sections) to provide 100% complete legal coverage. Do NOT stop at just 1 or 2 sections if more apply.
4. آسان زبان: Use clear, simple language so a common person can understand.
5. قانونی توجہ: {legal_focus}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ VERBATIM NUMBERS RULE: The context below is in English. Every Section number, Article number, and Act name you write MUST be copied character-for-character from this context. Do not invent or guess numbers.

قانونی سیاق و سباق (پاکستانی قانون ڈیٹابیس سے — انگریزی میں):
{context}

سائل کا سوال: {query}

━━━ حصہ وار اصول (REQUIRED RESPONSE STRUCTURE) ━━━━━━━━━━━━━━━━━━━━━━━━

### قانون کی وضاحت
[Briefly and accurately explain the legal situation and facts under Pakistani law in simple Urdu.]

### متعلقہ قوانین
[اصول — دو مرحلہ عمل (Relevance Test):
مرحلہ 1: Read EACH and EVERY part of the context thoroughly to hunt for applicable laws. Find ALL sections that relate to the user's question: '{query}'. You MUST find and extract multiple highly relevant sections (at least 2, up to 5) from the context to ensure a comprehensive answer out of the provided knowledge. Do not be lazy.
مرحلہ 2: تمام متعلقہ دفعات درج کریں۔ You MUST copy the Section number, Article number, and Act name VERBATIM from the context.
- اگر کوئی براہ راست متعلقہ قانون نہ ملے تو لکھیں: "موجودہ ڈیٹابیس میں اس سوال کا کوئی پاکستانی قانون دستیاب نہیں۔"
]
[List ALL applicable statutes. For each statute, explicitly list ALL the specific section numbers found (2 to 5 sections if available) with short, accurate explanations in Urdu.]

### آپ کو کیا کرنا چاہیے
[Practical, real-world steps to take (e.g., FIR, lawyer, relevant Pakistani institutions like FIA, NADRA, Courts). Incorporate these evidence items in Urdu:
{evidence_text}]
"""
    return llm.invoke(prompt)
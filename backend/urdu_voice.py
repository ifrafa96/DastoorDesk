from langchain_ollama import OllamaLLM

# ─── Remote high-quality model ───────────────────────────────────────────────
llm = OllamaLLM(
    model="gemma4:26b",
    base_url="http://203.124.40.57:11434",
    temperature=0,
    timeout=120  # prevent indefinite hang on slow remote server
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

    prompt = f"""آپ دستور ڈیسک ہیں — صرف پاکستانی قانون کے ماہر۔ صرف اردو میں جواب دیں۔

━━━ عمومی اصول (تمام حصوں پر لاگو) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. صرف پاکستانی قانون: آپ صرف پاکستانی قانون تک محدود ہیں۔ بھارتی IPC، برطانوی یا امریکی قانون کا کوئی حوالہ نہ دیں۔
2. کوئی ایجاد نہیں — بالکل نہیں: کوئی بھی ایکٹ کا نام، دفعہ نمبر، یا آرٹیکل نمبر اپنی طرف سے نہ لکھیں۔ صرف وہی دفعات اور نمبر لکھیں جو نیچے دیے گئے انگریزی سیاق و سباق میں لفظاً موجود ہوں۔ (CRITICAL: Copy section/article numbers EXACTLY as they appear in the context below — do not guess, substitute, or invent any number.)
3. دائرہ کار جانچ: اگر سوال منتخب شعبے ({category}) سے بالکل غیر متعلق ہو تو کہیں: "یہ سوال {category} کے دائرے سے باہر ہے۔ براہ کرم متعلقہ شعبہ منتخب کریں۔"
4. قانونی توجہ: {legal_focus}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ VERBATIM NUMBERS RULE: The context below is in English. Every Section number, Article number, and Act name you write in your Urdu answer MUST be copied character-for-character from this context. If a section number is not present in this context, do NOT write it.

قانونی سیاق و سباق (پاکستانی قانون ڈیٹابیس سے — انگریزی میں):
{context}

سائل کا سوال: {query}

━━━ حصہ وار اصول ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

###  قانون کی وضاحت
[اصول — دو مرحلہ عمل:
مرحلہ 1 (ربط جانچ): سیاق و سباق کے ہر حصے کو پڑھ کر خود سے پوچھیں: "کیا یہ دفعہ سائل کے اس مخصوص سوال کا براہ راست جواب دیتی ہے؟" اگر ہاں تو مرحلہ 2 پر جائیں۔ اگر دفعہ صرف ذیلی طور پر متعلق ہو، کسی اور ذیلی موضوع سے ہو، یا سوال سے براہ راست نہ ملے، تو اسے چھوڑ دیں۔
مرحلہ 2 (لفظاً نقل): صرف وہی دفعات درج کریں جو مرحلہ 1 میں کامیاب ہوئیں۔ دفعہ نمبر لفظاً سیاق و سباق سے نقل کریں — کوئی نمبر خود سے نہ گھڑیں۔
RELEVANCE TEST (apply in English): Only include a section if it DIRECTLY and SPECIFICALLY answers the user's question: "{query}". Skip sections about unrelated sub-topics even if they appear in the context.
- اگر کوئی براہ راست متعلقہ قانون نہ ملے تو لکھیں: "موجودہ ڈیٹابیس میں اس سوال کا کوئی پاکستانی قانون دستیاب نہیں۔"
]

**[ایکٹ 1 کا نام — سیاق و سباق سے]**
* **دفعہ [X]:** [یہ دفعہ سوال سے براہ راست کیسے متعلق ہے — مختصر وضاحت]
* **دفعہ [Y]:** [یہ دفعہ سوال سے براہ راست کیسے متعلق ہے]
(صرف وہی دفعات جو ربط جانچ میں کامیاب ہوئیں)

**[ایکٹ 2 کا نام — اگر سیاق و سباق میں اور سوال سے براہ راست متعلق ہو]**
* **دفعہ [A]:** [سوال سے براہ راست تعلق کی وضاحت]
* **دفعہ [B]:** [سوال سے براہ راست تعلق کی وضاحت]
(صرف وہی دفعات جو سوال کا براہ راست جواب دیتی ہوں)

**[سیاق و سباق میں موجود ہر اضافی براہ راست متعلقہ ایکٹ کے لیے یہ سلسلہ جاری رکھیں]**

###  آپ کا لائحہ عمل
[اصول: صرف پاکستانی اداروں اور طریقہ کار کا ذکر کریں: FIA، NADRA، PTA، سیشن کورٹ، ہائی کورٹ، کنزیومر کورٹ، SECP، SBP وغیرہ۔ غیر ملکی اداروں یا عمومی مشوروں کا ذکر نہ کریں۔]
1. [پہلا فوری قدم — مخصوص پاکستانی ادارہ]
2. [دوسرا قدم — ثبوت یا قانونی نوٹس]
3. [تیسرا قدم — عدالت یا ریگولیٹری ادارہ]

###  ثبوت کی فہرست
[اصول: صرف نیچے دی گئی فہرست استعمال کریں]
{evidence_text}
"""
    return llm.invoke(prompt)
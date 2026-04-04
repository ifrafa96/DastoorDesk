from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3", temperature=0)

def generate_urdu_response(query, context, category, evidence):
    # Specialized Legal logic for Urdu
    legal_focus = ""
    if "property" in category.lower() and ("kabza" in query or "قبضہ" in query):
        legal_focus = "خاص طور پر 'Illegal Dispossession Act 2005' اور اس کی دفعہ 3 پر توجہ دیں۔"
    
    prompt = f"""آپ دستور ڈیسک کے قانونی ماہر ہیں۔ صرف اردو میں جواب دیں۔
               لازمی ہدایات:
              آپ ایک سخت قانونی تحقیقی معاون ہیں۔
              جواب دینے کے لیے صرف فراہم کردہ LAW CONTEXT استعمال کریں۔
              ہر جواب میں متعلقہ ایکٹ کا نام اور دفعہ نمبر واضح طور پر لکھیں۔
              - اگر جواب LAW CONTEXT میں موجود نہ ہو تو صرف یہ لکھیں: "متعلقہ قانونی دفعہ موجودہ ڈیٹابیس میں دستیاب نہیں ہے۔"
              کسی بھی صورت میں بیرونی علم استعمال نہ کریں۔
              کسی بھی قانونی دفعہ، آرٹیکل یا حوالہ خود سے نہ گھڑیں۔
              
    قانونی توجہ: {legal_focus}
    تحقیق شدہ قانون: {context}
    سائل کا سوال: {query}
    
    براہ کرم درج ذیل ڈھانچے میں جواب دیں:
    ### ⚖️ قانون کی وضاحت
    * **قانون کا نام:** [Act Name]
    * **دفعات:** [Sections]
    * **خلاصہ:** [Simple Urdu explanation]

    ### 📋 آپ کا لائحہ عمل
    [3 practical steps]

    ### 📁 ثبوت کی فہرست
    {evidence}
    """
    return llm.invoke(prompt)
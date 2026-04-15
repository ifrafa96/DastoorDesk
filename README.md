# ⚖️ Dastoor Desk: AI-Powered Legal Assistant for Pakistan

**Dastoor Desk** is an advanced, multilingual legal intelligence platform designed to bridge the gap between complex Pakistani statutes and the common citizen. By utilizing an **Agentic RAG (Retrieval-Augmented Generation)** architecture, the system ensures that legal guidance is not just generated, but strictly grounded in verified Pakistani laws—including Property, Family, Labour, and Cybercrime statutes.



---

## 🌟 Key Features

* **Agentic Orchestration:** Powered by **LangGraph**, the system manages complex, state-aware legal reasoning workflows rather than simple linear chains.
* **Multilingual Support:** Seamlessly processes queries and generates structured legal advice in both **English and Urdu**.
* **Specialized Legal Domains:** Purpose-built agents for:
    * **Property Law** (Land Revenue Act, Registration Act)
    * **Family Law** (MFLO 1961, Family Courts Act)
    * **Labour Law** (Factories Act, Standing Orders)
    * **Cybercrime** (PECA 2016)
    * **Criminal & Traffic** (PPC, NHSO)
* **Voice Integration:** Integrated with **OpenAI Whisper** for high-accuracy voice-to-text transcription for mobile accessibility.
* **Quantitative Evaluation Matrix:** Includes a dedicated QA framework to measure system **Faithfulness**, **Relevance**, and **Latency**.

---

## 🏗️ System Architecture

Dastoor Desk moves beyond basic RAG by implementing an **Agentic Workflow**:

1.  **Input Node:** Accepts text or audio input.
2.  **Classification Node:** Routes the query to the specific legal department (e.g., Labour vs. Property).
3.  **Retriever Node:** Conducts a semantic search in **ChromaDB** using **MiniLM** embeddings with category-specific metadata filtering.
4.  **Reasoning Node:** A specialized legal agent synthesizes the law into three components:
    * **Legal Explanation:** Plain-language summary of the law.
    * **Applicable Laws:** Direct citations of sections and statutes.
    * **Action Plan:** Step-by-step guidance and an **Evidence Checklist**.

---

## 🛠️ Tech Stack

### **Backend (The Brain)**
* **Framework:** FastAPI (Asynchronous)
* **AI Orchestration:** LangGraph & LangChain
* **LLM:** Llama 3 / Gemma (via Ollama)
* **Vector DB:** ChromaDB
* **Embeddings:** HuggingFace (MiniLM-L6-v2)

### **Frontend (The Interface)**
* **Framework:** Next.js 15 (App Router)
* **Styling:** Tailwind CSS & Shadcn UI
* **Design Philosophy:** Minimalist, glassmorphism-inspired UI with high-end animations.

---

## 🚀 Getting Started

### **1. Prerequisites**
* Python 3.10+
* Node.js 18+
* [Ollama](https://ollama.com/) (installed and running)

### **2. Backend Setup**
```bash
# Clone the repository
git clone https://github.com/your-username/DastoorDesk.git
cd DastoorDesk/backend

# Create virtual environment
python -m venv dastoor_env
source dastoor_env/bin/activate  # On Windows: dastoor_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Ingest PDFs (Ensure PDFs are in /dastoor_pdfs subfolders)
python dastoor.py

# Run the server
python main.py
```

### **3. Frontend Setup**
```bash
cd ../frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```text
├── backend/
│   ├── dastoor_pdfs/         # Classified Pakistani Law PDFs
│   ├── dastoor_db/           # ChromaDB Vector Store
│   ├── graph_engine.py       # LangGraph Orchestration logic
│   ├── dastoor.py            # Ingestion & Metadata logic
│   ├── main.py               # FastAPI Endpoints
│   └── evaluation_matrix.py  # Quantitative testing suite
├── frontend/
│   ├── app/                  # Next.js App Router
│   ├── components/           # UI Components (Apple-like aesthetic)
│   └── lib/                  # API communication
└── README.md
```

---

## 📊 Performance & Evaluation
Dastoor Desk is rigorously tested using a **Quantitative Evaluation Matrix**. We measure:
* **Context Precision:** Accuracy of the retriever in finding the correct law.
* **Faithfulness:** Ensuring the LLM does not hallucinate beyond the retrieved legal chunks.
* **Multilingual Accuracy:** Comparing performance between English and Urdu response generation.

---

## 📜 Legal Disclaimer
Dastoor Desk is an AI-powered educational tool designed to provide legal information and simplify complex statutes. It **does not** constitute formal legal advice. For formal litigation or court cases, users should consult a qualified legal professional.

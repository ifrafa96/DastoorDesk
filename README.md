# ⚖️ Dastoor Desk: AI-Powered Legal Intelligence for Pakistan

**Dastoor Desk** is a state-of-the-art, multilingual legal assistance platform. It uses an **Agentic RAG (Retrieval-Augmented Generation)** architecture to provide Pakistani citizens with structured, verified, and grounded legal guidance. Unlike standard chatbots, Dastoor Desk classifies queries and retrieves context from a specialized database of over **3,300+ legal chunks** derived from official Pakistani statutes.



---

## 📚 Comprehensive Legal Coverage
The system is currently indexed with the following official Pakistani laws and ordinances:

| Department | Primary Statutes & Acts Covered |
| :--- | :--- |
| **🏠 Property** | Land Revenue Act 1967, Registration Act 1908, Transfer of Property Act 1882 |
| **👨‍👩‍👧 Family** | Muslim Family Laws Ordinance 1961, Family Courts Act 1964, Guardians & Wards Act |
| **🛠️ Labour** | Factories Act 1934, Payment of Wages Act 1936, Standing Orders Ordinance 1968 |
| **💻 Cybercrime** | Prevention of Electronic Crimes Act (PECA) 2016, FIA Act |
| **⚖️ Criminal** | Pakistan Penal Code (PPC), Code of Criminal Procedure (CrPC) |
| **🚦 Traffic** | National Highways Safety Ordinance (NHSO), Motor Vehicle Ordinance |
| **🛡️ Consumer** | Punjab/Sindh/KPK/Islamabad Consumer Protection Acts |
| **📜 Constitutional**| The Constitution of the Islamic Republic of Pakistan |

---

## 🏗️ Technical Architecture: The Agentic Workflow
Dastoor Desk utilizes **LangGraph** to manage a non-linear, stateful workflow that ensures high accuracy:

1.  **Input Layer:** Processes text or voice (transcribed via **OpenAI Whisper**).
2.  **Orchestrator (The Classifier):** Identifies the legal domain and province to apply metadata filters.
3.  **Knowledge Retrieval:** Queries **ChromaDB** using **MiniLM-L6-v2** embeddings. It searches specifically within the folder/category identified by the classifier.
4.  **Reasoning Engine:** A specialized LLM (Llama 3/Gemma via Ollama) processes the law chunks to generate:
    * **Legal Explanation:** Simple summary of the user's rights.
    * **Applicable Laws:** Exact citations of Sections and Chapters.
    * **Action Plan:** Step-by-step procedure (e.g., how to file a "Suit" or "FIR").
    * **Evidence Checklist:** Dynamic list of required documents (e.g., Nikahnama, Fard, Salary Slips).

---

## 🛠️ Tech Stack

* **AI Framework:** LangGraph, LangChain, Ollama.
* **Vector Database:** ChromaDB (with Metadata Filtering).
* **Backend:** FastAPI (Python), Asynchronous processing.
* **Frontend:** Next.js 15, React, Tailwind CSS, Shadcn UI.
* **Voice:** OpenAI Whisper (Local Integration).
* **Evaluation:** Custom Quantitative Evaluation Matrix (Faithfulness, Relevance, Latency).

---

## 🚀 Installation & Setup

### **1. Backend Configuration**
```bash
# Clone the repository
git clone https://github.com/your-username/DastoorDesk.git
cd DastoorDesk/backend

# Initialize virtual environment
python -m venv dastoor_env
source dastoor_env/bin/activate # Windows: .\dastoor_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Ingest Legal PDFs (Ensure files are in /dastoor_pdfs/{category})
python dastoor.py

# Launch FastAPI Server
python main.py
```

### **2. Frontend Configuration**
```bash
cd ../frontend
npm install
npm run dev
```

---

## 📊 Evaluation & Quality Assurance
The project includes an **`evaluation_matrix.py`** script that runs a "Ground Truth" test suite. It calculates:
* **Overall Accuracy:** Percentage of correct legal citations.
* **Context Retrieval Rate:** Success rate of finding the correct PDF chunk.
* **Language-Specific Performance:** Comparative accuracy between English and Urdu responses.
* **System Latency:** Average time taken to generate a multi-agent response.

---

## 📁 Project Structure
```text
├── backend/
│   ├── dastoor_pdfs/         # Organized sub-folders for all 7+ Law Departments
│   ├── dastoor_db/           # Persistent ChromaDB Vector Store (3,300+ chunks)
│   ├── graph_engine.py       # LangGraph state & node definitions
│   ├── tools_library.py      # Custom Search & Retrieval tools
│   ├── main.py               # FastAPI Endpoints for UI communication
│   └── evaluation_matrix.py  # Quantitative testing framework
├── frontend/
│   ├── app/                  # Next.js App Router (UI & Animations)
│   └── components/           # Reusable legal UI components
└── README.md
```

---

## 📜 Legal Disclaimer
Dastoor Desk is an AI-powered educational resource. It provides information based on processed legal documents but does not constitute professional legal advice. Users are advised to verify details with a qualified advocate for court proceedings.

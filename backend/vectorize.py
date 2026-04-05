import os
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings # Updated import
from langchain_chroma import Chroma                 # Modern partner package
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ─── MUST match the model used in main.py exactly ────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# ─── Map raw CSV law_category → frontend department IDs ─────────────────────
# Frontend sends: property | cybercrime | traffic | consumer |
#                 family   | labour     | criminal | constitutional
CATEGORY_MAP = {
    # Cybercrime / FIA
    "peca":              "cybercrime",
    "fia":               "cybercrime",
    # Criminal
    "ppc":               "criminal",
    # Constitutional
    "constitution":      "constitutional",
    # Consumer
    "consumerprotection": "consumer",
    # Traffic / Highways
    "highways":          "traffic",
    "dlarules":          "traffic",
    # Labour / NHSO (National Health Services — closest to labour/consumer)
    "nhso":              "consumer",
    # Fallback: keep as-is (lowercased)
}

def map_category(raw: str) -> str:
    """Normalize a raw CSV category to a frontend department ID."""
    key = str(raw).lower().strip()
    # Strip spaces/underscores for fuzzy key matching
    key_clean = key.replace(" ", "").replace("_", "")
    return CATEGORY_MAP.get(key_clean, CATEGORY_MAP.get(key, key))

def create_vector_db():
    csv_file = "dastoor_desk_dataset.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found in {os.getcwd()}")
        return

    print("🚀 Loading processed chunks from CSV...")
    df = pd.read_csv(csv_file)
    print(f"📄 Loaded {len(df)} raw rows.")

    # ── Step 1: CSV rows → LangChain Documents (with category mapping) ──────
    raw_documents = []
    category_counts: dict = {}
    for _, row in df.iterrows():
        mapped_cat = map_category(str(row['law_category']))
        category_counts[mapped_cat] = category_counts.get(mapped_cat, 0) + 1
        raw_documents.append(Document(
            page_content=str(row['text']),
            metadata={
                "category": mapped_cat,
                "source":   str(row['source_file']),
                "raw_category": str(row['law_category'])   # keep original for debug
            }
        ))
    print("📊 Category distribution after mapping:")
    for cat, count in sorted(category_counts.items()):
        print(f"   {cat}: {count} rows")

    # ── Step 2: Chunk large documents ─────────────────────────────────────
    # chunk_size=500 keeps 2-3 legal sentences per chunk.
    # Urdu full-stop (۔) is included as a separator alongside Latin punctuation.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "۔", ".", "،", ",", " ", ""]
    )

    split_docs = splitter.split_documents(raw_documents)
    print(f"✂️  Split into {len(split_docs)} chunks (from {len(raw_documents)} raw rows).")

    # ── Step 3: Embed with the SAME model used at query time ──────────────
    print(f"🧠 Loading embedding model: {EMBEDDING_MODEL}")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # ── Step 4: (Re)create vector DB ──────────────────────────────────────
    db_path = "./dastoor_db"
    if os.path.exists(db_path):
        import shutil
        print(f"🗑️  Removing stale DB at {db_path} ...")
        shutil.rmtree(db_path)

    print("💾 Building ChromaDB vector store...")
    vector_db = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=db_path
    )

    print(f"✅ Vector DB created at {db_path} — {len(split_docs)} chunks indexed.")
    return vector_db

if __name__ == "__main__":
    create_vector_db()
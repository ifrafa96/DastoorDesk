import os
import time
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Local Project Imports
from logger_config import logger
from tools_library import LegalTools
from graph_engine import create_dastoor_graph

def run_evaluation_matrix(csv_path="legal_ground_truth.csv"):
    """
    Runs a quantitative test suite against the Dastoor Desk Brain 
    to calculate accuracy and performance metrics for English & Urdu.
    """
    
    # 1. Component Initialization
    logger.info("[EVALUATION] Initializing components for testing...")
    
    # Initialize Embeddings and Vector DB
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="./dastoor_db", embedding_function=embeddings)
    
    # Initialize Legal Tools and the Compiled Graph
    legal_tools = LegalTools(vector_db)
    brain = create_dastoor_graph(vector_db, legal_tools)

    # 2. Safety Check for Ground Truth File
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found.")
        print("Please create a CSV with 'Question', 'Category', 'Expected Law', and 'Language' columns.")
        return

    # 3. Load the Test Dataset
    test_data = pd.read_csv(csv_path)
    results = []

    print(f"🚀 Starting Quantitative Evaluation on {len(test_data)} queries...")
    print("-" * 50)

    for index, row in test_data.iterrows():
        start_time = time.time()
        
        # Prepare inputs including the 'language' column from CSV
        query_lang = str(row.get('Language', 'en')).lower()
        inputs = {
            "query": row['Question'], 
            "language": "ur" if "urdu" in query_lang else "en", 
            "category": row.get('Category', 'property').lower()
        }
        
        try:
            # Execute the AI Graph workflow
            final_state = brain.invoke(inputs)
            latency = round(time.time() - start_time, 2)
            
            # 4. Quantitative Metrics Calculation
            ai_answer = final_state.get('response', "").lower()
            expected_law = str(row['Expected Law']).lower()
            
            # Metric 1: Keyword Match (Check if law name exists in AI response)
            score_relevance = 1 if expected_law in ai_answer else 0
            
            # Metric 2: Context Retrieval Success
            context_found = 1 if final_state.get('context') else 0

            # Metric 3: Evidence Checklist Presence
            has_evidence = 1 if final_state.get('evidence') else 0

            results.append({
                "Question": row['Question'],
                "Language": query_lang.capitalize(),
                "Category": inputs['category'],
                "Expected_Law": expected_law,
                "Score_Relevance": score_relevance,
                "Context_Found": context_found,
                "Has_Evidence": has_evidence,
                "Latency_Sec": latency
            })
            
            status_icon = "✅" if score_relevance == 1 else "❌"
            print(f"{status_icon} [{query_lang.upper()}] Query {index+1}: {row['Question'][:30]}... | {latency}s")

        except Exception as e:
            print(f"❗ Error testing query at index {index}: {e}")

    # 5. Compile the Matrix & Generate Language-Wise Statistics
    matrix_df = pd.DataFrame(results)
    
    overall_accuracy = matrix_df['Score_Relevance'].mean() * 100
    avg_latency = matrix_df['Latency_Sec'].mean()
    
    # Grouping by Language for more detailed analysis
    lang_stats = matrix_df.groupby('Language').agg({
        'Score_Relevance': 'mean',
        'Latency_Sec': 'mean'
    })
    lang_stats['Score_Relevance'] *= 100

    print("\n" + "="*50)
    print("📊 FINAL QUANTITATIVE EVALUATION MATRIX")
    print("="*50)
    print(f"Total Queries Processed: {len(matrix_df)}")
    print(f"Overall System Accuracy:  {overall_accuracy:.2f}%")
    print(f"Average System Latency:   {avg_latency:.2f} seconds")
    print("-" * 50)
    
    for lang, row in lang_stats.iterrows():
        print(f"{lang} Accuracy:         {row['Score_Relevance']:.2f}%")
        print(f"{lang} Avg Latency:      {row['Latency_Sec']:.2f}s")
    
    print("="*50)

    # Save detailed results
    matrix_df.to_csv("evaluation_results_summary.csv", index=False)
    print("\n📝 Detailed report saved to 'evaluation_results_summary.csv'")

if __name__ == "__main__":
    run_evaluation_matrix()
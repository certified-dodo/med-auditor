import os
import chromadb
from sentence_transformers import SentenceTransformer

def initialize_vector_db():
    """Initialize and return the ChromaDB client and collection."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "chroma_db")
    
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=db_path)
    
    # Get the collection
    try:
        collection = client.get_collection(name="text_chunks")
        print(f"Successfully connected to ChromaDB collection: text_chunks")
        return client, collection
    except Exception as e:
        print(f"Error accessing ChromaDB collection: {e}")
        return None, None

def query_similar_medical_records(collection, query_text, model, n_results=5):
    """Query the vector database to find similar medical records."""
    # Create embedding for the query text
    query_embedding = model.encode([query_text]).tolist()
    
    # Query the collection
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    return results

def main():
    # Initialize sentence transformer model
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize vector database
    print("Connecting to vector database...")
    _, collection = initialize_vector_db()
    
    if collection is None:
        print("Failed to connect to ChromaDB. Make sure you've run text_embedder.py first.")
        return
    
    # Test query for diabetic patient
    test_query = """
    CHART SUBMISSION
    PATIENT: MRN-91283
    DATE OF SERVICE: 03/15/2024
    SERVICE TYPE: Skilled Nursing - Diabetic care
    VISIT DURATION: 55 minutes
    VITAL SIGNS: BP 165/95, HR 88, RR 18, Temp 98.8F, O2 sat 96%
    SERVICES PROVIDED: Wound care to R foot ulcer. Diabetic foot assessment. Blood glucose monitoring. Caregiver education.
    MEDICATIONS ADMINISTERED/REVIEWED: Lantus 30 units qHS, Novolog sliding scale, Metformin 1000mg daily, Lisinopril 20mg daily
    PATIENT STATUS: Blood glucose elevated (fasting 210, pre-lunch 188). Wagner Grade 1 ulcer to R foot. Visual impairment affecting self-monitoring.
    FOLLOW-UP: Referral to diabetic educator initiated.
    BILLING CODE: G0299
    """
    
    print("\nTesting query for diabetic patient...")
    results = query_similar_medical_records(collection, test_query, model)
    
    print("\nRelevant medical record chunks:")
    for i, doc in enumerate(results["documents"][0]):
        print(f"\nResult {i+1} (distance: {results['distances'][0][i]:.4f}):")
        print(doc[:300] + "...")
    
    # Test query for CHF patient
    test_query = """
    CHART SUBMISSION
    PATIENT: MRN-65441
    DATE OF SERVICE: 03/15/2024
    SERVICE TYPE: Skilled Nursing - CHF monitoring
    VISIT DURATION: 50 minutes
    VITAL SIGNS: BP 142/88, HR 82, RR 20, Temp 99.1F, O2 sat 92%
    SERVICES PROVIDED: Cardiopulmonary assessment. Medication compliance review. Patient education on daily weights.
    MEDICATIONS ADMINISTERED/REVIEWED: Lasix 40mg daily, Metoprolol 50mg BID, Lisinopril 10mg daily, KCl 20mEq daily
    PATIENT STATUS: SOB on exertion. Bilateral LE edema +2. Gained 4lbs in 3 days. Lung crackles present.
    FOLLOW-UP: Called MD for medication adjustment.
    BILLING CODE: G0299
    """
    
    print("\nTesting query for CHF patient...")
    results = query_similar_medical_records(collection, test_query, model)
    
    print("\nRelevant medical record chunks:")
    for i, doc in enumerate(results["documents"][0]):
        print(f"\nResult {i+1} (distance: {results['distances'][0][i]:.4f}):")
        print(doc[:300] + "...")

if __name__ == "__main__":
    main() 
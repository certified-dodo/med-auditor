import os
import chromadb
from sentence_transformers import SentenceTransformer
import textwrap
import uuid
import time

def create_text_chunks(text, chunk_size=500):
    """Split text into chunks of approximately chunk_size characters."""
    # Use textwrap to create chunks of approximately chunk_size characters
    chunks = textwrap.wrap(text, width=chunk_size, break_long_words=False, break_on_hyphens=False)
    return chunks

def process_file(file_path, chunk_size=500, model_name="all-MiniLM-L6-v2"):
    """Process file contents, create embeddings and store in ChromaDB."""
    # Initialize embedding model
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    
    # Initialize ChromaDB
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
    print(f"Initializing ChromaDB at: {db_path}")
    client = chromadb.PersistentClient(path=db_path)
    
    # Create or get collection
    collection_name = "text_chunks"
    try:
        # Try to get existing collection or create new one
        collection = client.get_or_create_collection(name=collection_name)
        print(f"Using collection: {collection_name}")
    except Exception as e:
        print(f"Error with collection: {e}")
        # If collection exists but with different settings, recreate it
        if collection_name in [c.name for c in client.list_collections()]:
            client.delete_collection(name=collection_name)
        collection = client.create_collection(name=collection_name)
    
    # Read file
    print(f"Reading file: {file_path}")
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Create chunks
    chunks = create_text_chunks(content, chunk_size)
    print(f"Created {len(chunks)} chunks of ~{chunk_size} characters")
    
    # Create embeddings and store in ChromaDB
    print("Generating embeddings...")
    start_time = time.time()
    
    # Generate embeddings for all chunks at once (more efficient)
    embeddings = model.encode(chunks)
    print(f"Embeddings generated in {time.time() - start_time:.2f} seconds")
    
    # Add to collection with metadata
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    metadata_list = [{"source": file_path, "index": i, "chunk_size": chunk_size} 
                   for i in range(len(chunks))]
    
    print("Adding to ChromaDB...")
    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=chunks,
        metadatas=metadata_list
    )
    
    print(f"Successfully added {len(chunks)} chunks to ChromaDB")
    return collection, chunks, model

def query_similar_chunks(collection, query_text, model, n_results=3):
    """Query database for chunks similar to the query text."""
    query_embedding = model.encode([query_text]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results

def main():
    # File path
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "standardized_medical_records.txt")
    
    # Process file and get collection, chunks, and model
    collection, chunks, model = process_file(file_path)
    
    # Display the chunks
    print("\nSample chunks created:")
    for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
        print(f"Chunk {i+1} ({len(chunk)} chars): {chunk[:100]}...")
    
    # Perform queries
    queries = [
        "diabetic patient with foot ulcer",
        "congestive heart failure with fluid retention",
        "COPD management and oxygen therapy",
        "post-operative wound care after knee replacement",
        "palliative care for pain management",
        "stage 3 pressure ulcer treatment",
        "stroke recovery therapy",
        "catheter care and UTI prevention"
    ]
    
    for query in queries:
        print(f"\nPerforming query: '{query}'")
        results = query_similar_chunks(collection, query, model)
        
        # Display results
        print("\nResults:")
        for i, (doc, score) in enumerate(zip(results["documents"][0], results["distances"][0])):
            print(f"Result {i+1} (distance: {score:.4f}):")
            print(f"{doc[:200]}...\n")

if __name__ == "__main__":
    main() 
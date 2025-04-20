# Text Embedding with ChromaDB

This implementation demonstrates how to chunk text into ~500 character segments, generate embeddings, and store them in a vector database (ChromaDB).

## Features

- Text chunking with configurable chunk size
- Embedding generation using Sentence Transformers
- Persistent storage with ChromaDB
- Semantic search capabilities

## Setup

1. Ensure you've activated the virtual environment:
   ```bash
   source ~/.venvs/med-auditor-venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install chromadb sentence-transformers
   ```

## Usage

The main script is `text_embedder.py`, which:

1. Reads text from a file
2. Splits it into ~500 character chunks
3. Generates embeddings using a pre-trained model
4. Stores the embeddings in ChromaDB
5. Provides a simple query interface

Example:
```bash
python backend/text_embedder.py
```

## How It Works

1. **Text Chunking**:
   - The script uses Python's `textwrap` to break text into ~500 character segments
   - Preserves word boundaries (doesn't break in the middle of words)

2. **Embedding Generation**:
   - Uses `sentence-transformers` with the "all-MiniLM-L6-v2" model
   - This model creates 384-dimensional embeddings that capture semantic meaning

3. **Vector Database Storage**:
   - ChromaDB stores embeddings with associated metadata
   - Data is persisted to disk at `backend/chroma_db/`
   - Each chunk is stored with source information and position metadata

4. **Semantic Search**:
   - Query text is converted to an embedding
   - ChromaDB finds the most similar chunks based on vector similarity

## Customization

You can modify:
- The chunk size (default: 500 characters)
- The embedding model
- The number of results returned in queries

## Extending

This implementation can be extended to:
- Process multiple documents
- Implement more advanced chunking strategies
- Add a REST API interface
- Integrate with other vector databases 
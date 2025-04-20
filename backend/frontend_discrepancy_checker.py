import os
import re
import json
import chromadb
from openai import AzureOpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
API_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')

# Create Azure OpenAI client
client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=API_ENDPOINT,
    api_key=API_KEY
)

def initialize_vector_db():
    """Initialize and return the ChromaDB client and collection."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "chroma_db")
    
    client = chromadb.PersistentClient(path=db_path)
    
    try:
        collection = client.get_collection(name="text_chunks")
        print(f"Successfully connected to ChromaDB collection: text_chunks")
        return client, collection
    except Exception as e:
        print(f"Error accessing ChromaDB collection: {e}")
        return None, None

def query_similar_medical_records(collection, chart_text, model, n_results=5):
    """Query the vector database to find similar medical records."""
    query_embedding = model.encode([chart_text]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    return results

def get_chart_fields(chart_text):
    """Parse chart text into structured fields with line numbers."""
    lines = chart_text.strip().split('\n')
    chart_fields = []
    
    for i, line in enumerate(lines):
        line_number = i + 1  # 1-indexed line numbers
        
        if line.strip() == "" or "CHART SUBMISSION" in line:
            continue
            
        if ":" in line:
            parts = line.split(":", 1)
            title = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ""
            
            field = {
                "title": title,
                "value": value,
                "line": line_number
            }
            chart_fields.append(field)
        else:
            field = {
                "title": "CONTENT",
                "value": line.strip(),
                "line": line_number
            }
            chart_fields.append(field)
    
    return chart_fields

def find_discrepancies(chart, medical_record):
    """Use Azure OpenAI to identify discrepancies between chart and medical record."""
    prompt = f"""
You are a medical auditor reviewing home health nursing documentation. 
Compare the following chart submission against the standardized medical record for discrepancies.
For each field in the chart, identify if there are any discrepancies.

STANDARDIZED MEDICAL RECORD:
{medical_record}

CHART SUBMISSION:
{chart}

Format your response as a JSON array with objects for each discrepancy:
[
  {{
    "field": "The field title (e.g., 'VITAL SIGNS', 'MEDICATIONS ADMINISTERED/REVIEWED')",
    "discrepancy": "Clear description of what is incorrect",
    "correct_value": "What the value should be according to the medical record"
  }}
]
"""
    
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise medical auditing assistant that identifies discrepancies between medical charts and records."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=DEPLOYMENT
        )
        
        result = response.choices[0].message.content
        
        try:
            # Extract JSON from response
            json_text = re.search(r'(\[[\s\S]*\])', result).group(1)
            return json.loads(json_text)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {result}")
            return []
            
    except Exception as e:
        print(f"Error calling Azure OpenAI API: {e}")
        return []

def process_chart(chart_text, collection, model):
    """Process a single chart and return structured output with discrepancies."""
    # Parse chart into structured fields
    chart_fields = get_chart_fields(chart_text)
    
    # Query similar medical records
    results = query_similar_medical_records(collection, chart_text, model)
    
    if not results["documents"][0]:
        return chart_fields
    
    # Get discrepancies
    medical_record = results["documents"][0][0]
    discrepancies = find_discrepancies(chart_text, medical_record)
    
    # Add discrepancies to fields
    for field in chart_fields:
        for discrepancy in discrepancies:
            if field["title"] == discrepancy["field"]:
                field["discrepancy"] = discrepancy["discrepancy"]
                field["correct_value"] = discrepancy["correct_value"]
    
    return chart_fields

def process_chart_from_memory(chart_text, medical_record_text, model):
    """Process a chart using in-memory medical record data."""
    # Parse chart into structured fields
    chart_fields = get_chart_fields(chart_text)
    
    # Get discrepancies
    discrepancies = find_discrepancies(chart_text, medical_record_text)
    
    # Add discrepancies to fields
    for field in chart_fields:
        for discrepancy in discrepancies:
            if field["title"] == discrepancy["field"]:
                field["discrepancy"] = discrepancy["discrepancy"]
                field["correct_value"] = discrepancy["correct_value"]
    
    return chart_fields

def main():
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Connecting to vector database...")
    _, collection = initialize_vector_db()
    
    if collection is None:
        print("Failed to connect to ChromaDB.")
        return
    
    # Sample chart text
    sample_chart = """CHART SUBMISSION
PATIENT: MRN-91283
DATE OF SERVICE: 03/15/2024
SERVICE TYPE: Skilled Nursing - Diabetic care
VITAL SIGNS: BP 165/95, HR 88, RR 18, Temp 98.8F, O2 sat 96%
MEDICATIONS ADMINISTERED/REVIEWED: Lantus 30 units qHS, Novolog sliding scale, Metformin 1000mg daily, Lisinopril 20mg daily"""
    
    # Process the chart
    result = process_chart(sample_chart, collection, model)
    
    # Output the result as JSON
    print(json.dumps(result, indent=2))
    
    # Example of using in-memory data
    try:
        from test_data import medical_records, charts
        
        # Process first chart against corresponding medical record
        first_mrn = list(charts.keys())[0]
        chart_text = charts[first_mrn]
        medical_record_text = medical_records[first_mrn]
        
        print("\nProcessing in-memory chart data...")
        in_memory_result = process_chart_from_memory(chart_text, medical_record_text, model)
        print(json.dumps(in_memory_result, indent=2))
        
    except ImportError:
        print("test_data.py not found. Skipping in-memory example.")

if __name__ == "__main__":
    main() 
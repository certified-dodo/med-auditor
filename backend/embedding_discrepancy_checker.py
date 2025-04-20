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

def load_charts(file_path):
    """Load and parse standardized charts with line numbers."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Split by "CHART SUBMISSION" to separate patients
    charts = []
    current_chart = []
    start_line = 0
    chart_starts = []
    
    for i, line in enumerate(lines):
        if "CHART SUBMISSION" in line and current_chart:
            charts.append(''.join(current_chart))
            chart_starts.append(start_line)
            current_chart = [line]
            start_line = i + 1
        elif "CHART SUBMISSION" in line:
            current_chart = [line]
            start_line = i + 1
        else:
            current_chart.append(line)
    
    if current_chart:
        charts.append(''.join(current_chart))
        chart_starts.append(start_line)
    
    # Parse each chart and extract MRN
    charts_dict = {}
    for i, chart in enumerate(charts):
        match = re.search(r'PATIENT:\s+MRN-(\d+)', chart)
        if match:
            mrn = match.group(1)
            charts_dict[mrn] = {
                'content': chart,
                'start_line': chart_starts[i]
            }
    
    return charts_dict

def extract_patient_mrn_from_medical_record(text):
    """Extract the MRN from a medical record chunk."""
    match = re.search(r'PATIENT_ID:\s+MRN-(\d+)', text)
    if match:
        return match.group(1)
    return None

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

def query_similar_medical_records(collection, chart_text, model, n_results=5):
    """Query the vector database to find similar medical records."""
    # Create embedding for the chart text
    query_embedding = model.encode([chart_text]).tolist()
    
    # Query the collection
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    return results

def find_discrepancies_with_embeddings(chart, embeddings_results, chart_start_line):
    """Use Azure OpenAI to identify discrepancies between chart and relevant medical record chunks."""
    
    # Extract documents from the query results
    relevant_chunks = embeddings_results["documents"][0]
    
    # Join the relevant chunks into a single text
    medical_record_text = "\n".join(relevant_chunks)
    
    # Create prompt for the API
    prompt = f"""
You are a medical auditor reviewing home health nursing documentation. 
Compare the following chart submission against the relevant sections of the standardized medical record for discrepancies.
Return ONLY the discrepancies found, with the specific line number in the chart where each discrepancy occurs.

STANDARDIZED MEDICAL RECORD SECTIONS:
{medical_record_text}

CHART SUBMISSION:
{chart}

For example output:
{{
  "discrepancies": [
    {{
      "line_number": 5,
      "discrepancy": "O2 saturation incorrect",
      "correct_value": "94%"
    }},
    {{
      "line_number": 7,
      "discrepancy": "Metoprolol dose incorrect",
      "correct_value": "25mg BID"
    }}
  ]
}}
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
        
        # Parse the JSON response
        try:
            # Extract JSON from response (it might have extra text)
            json_text = re.search(r'({[\s\S]*})', result).group(1)
            discrepancies_data = json.loads(json_text)
            
            # Adjust line numbers to be relative to the file
            if 'discrepancies' in discrepancies_data:
                for item in discrepancies_data['discrepancies']:
                    if 'line_number' in item:
                        item['line_number'] = item['line_number'] + chart_start_line - 1
            
            return discrepancies_data
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {result}")
            return {"discrepancies": []}
            
    except Exception as e:
        print(f"Error calling Azure OpenAI API: {e}")
        return {"discrepancies": []}

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize sentence transformer model
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize vector database
    print("Connecting to vector database...")
    _, collection = initialize_vector_db()
    
    if collection is None:
        print("Failed to connect to ChromaDB. Make sure you've run text_embedder.py first.")
        return
    
    # Load charts
    charts_path = os.path.join(script_dir, 'standardized_charts.txt')
    charts = load_charts(charts_path)
    
    print(f"Loaded {len(charts)} charts.")
    
    # Find matching patients and check for discrepancies
    all_discrepancies = []
    
    # List of MRNs to process (just a few for testing)
    test_mrns = ["91283", "65441", "78392"]
    
    for mrn in test_mrns:
        if mrn in charts:
            print(f"Checking MRN-{mrn}...")
            chart_data = charts[mrn]
            
            # Query vector DB for similar medical records
            similar_records = query_similar_medical_records(
                collection, 
                chart_data['content'],
                model
            )
            
            # Find discrepancies using embeddings
            discrepancies = find_discrepancies_with_embeddings(
                chart_data['content'], 
                similar_records,
                chart_data['start_line']
            )
            
            if 'discrepancies' in discrepancies and discrepancies['discrepancies']:
                all_discrepancies.extend(discrepancies['discrepancies'])
                print(f"Found {len(discrepancies['discrepancies'])} discrepancies for MRN-{mrn}")
            else:
                print(f"No discrepancies found for MRN-{mrn}")
        else:
            print(f"WARNING: No chart found for MRN-{mrn}")
    
    # Print all discrepancies
    if all_discrepancies:
        print("\nALL DISCREPANCIES FOUND:")
        for item in all_discrepancies:
            if 'line_number' in item and 'discrepancy' in item and 'correct_value' in item:
                print(f"Line {item['line_number']}: {item['discrepancy']} (Should be: {item['correct_value']})")
            else:
                print(f"Malformed discrepancy item: {item}")
    else:
        print("\nNo discrepancies found in any chart.")

if __name__ == "__main__":
    main() 
import os
import re
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

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

def load_medical_records(file_path):
    """Load and parse standardized medical records."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split by double newline to separate patients
    patient_records = content.strip().split('\n\n')
    
    # Parse each patient record
    records_dict = {}
    for record in patient_records:
        # Extract patient ID
        match = re.search(r'PATIENT_ID:\s+MRN-(\d+)', record)
        if match:
            mrn = match.group(1)
            records_dict[mrn] = record
    
    return records_dict

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

def find_discrepancies(chart, medical_record, chart_start_line):
    """Use Azure OpenAI to identify discrepancies between chart and medical record."""
    
    # Create prompt for the API
    prompt = f"""
You are a medical auditor reviewing home health nursing documentation. 
Compare the following chart submission against the standardized medical record for discrepancies.
Return ONLY the discrepancies found, with the specific line number in the chart where each discrepancy occurs.

STANDARDIZED MEDICAL RECORD:
{medical_record}

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
    
    # Load files
    medical_records_path = os.path.join(script_dir, 'standardized_medical_records.txt')
    charts_path = os.path.join(script_dir, 'standardized_charts.txt')
    
    medical_records = load_medical_records(medical_records_path)
    charts = load_charts(charts_path)
    
    print(f"Loaded {len(medical_records)} medical records and {len(charts)} charts.")
    
    # Find matching patients and check for discrepancies
    all_discrepancies = []
    
    for mrn, chart_data in charts.items():
        if mrn in medical_records:
            print(f"Checking MRN-{mrn}...")
            
            discrepancies = find_discrepancies(
                chart_data['content'], 
                medical_records[mrn],
                chart_data['start_line']
            )
            
            if 'discrepancies' in discrepancies and discrepancies['discrepancies']:
                all_discrepancies.extend(discrepancies['discrepancies'])
                print(f"Found {len(discrepancies['discrepancies'])} discrepancies for MRN-{mrn}")
            else:
                print(f"No discrepancies found for MRN-{mrn}")
        else:
            print(f"WARNING: No matching medical record found for chart MRN-{mrn}")
    
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
import subprocess
import json
import time
# Open the JSON file and load queries
with open('s2/s2_query.json') as json_file:
    data = json.load(json_file)
queries = data['queries']

# Function to execute grep command
# Function to execute findstr command
def execute_findstr_query(query):
    start_time = time.time()
    try:
        findstr_output = subprocess.check_output(['findstr', '/r', '^' + query, r's2\s2_doc.json'], text=True)
        matched_documents = [int(line.split()[1]) for line in findstr_output.strip().split('\n')]
    except subprocess.CalledProcessError:
        matched_documents = []
    end_time = time.time()
    return matched_documents, end_time - start_time

# Execute each query and record timings
for query in queries:
    findstr_result, findstr_time = execute_findstr_query(query['query'])
    print(f"Findstr Query: {query['query']}")
    print(f"Findstr Result: {findstr_result}")
    print(f"Time taken (findstr): {findstr_time} seconds\n")



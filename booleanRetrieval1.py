

from concurrent.futures import TimeoutError
import json
import time
import cProfile
import pstats
#from memory_profiler import profile


# Open the JSON file and load queries
with open('s2/s2_query.json') as json_file:
    data = json.load(json_file)
queries = data['queries']

# Function to read postings from file
def read_postings(file_path):
    postings_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # Split the line by tabs
                term = line.strip().split('\t')[0]
                doc_id = line.strip().split('\t')
                # Add the term and its associated document ID to the dictionary
                for word in doc_id[1:]:
                    postings_dict.setdefault(term, []).append(word)
            except ValueError:
                # Skip lines that do not have the expected format
                continue
    return postings_dict

# Read postings
posting_start_time = time.time()
postings_file = 's2/intermediate/postings.tsv'
postings_dict = read_postings(postings_file)
elapsed_posting_time = time.time() - posting_start_time
print("Posting time:")
print(elapsed_posting_time)

# Function to execute boolean queries
# Function to execute boolean queries

def execute_boolean_query(query):
    start_time = time.time()  # Record start time 
    query_terms = query.split(" ")  # Split query into terms
    relevant_docs = set(postings_dict.get(query_terms[0], []))

    # Apply AND and OR operations
    for i in range(1, len(query_terms), 1):
        relevent_docs = set(postings_dict.get(query_terms[i],[]))

    elapsed_time = time.time() - start_time  # Calculate elapsed time
    return elapsed_time


# Execute queries and record timings
# Execute queries and record timings
query_timings = {}
for query_info in queries:
    query = query_info['query']
    try:
        #start_time = time.time_ns()  # Record start time
        elapsed_time = execute_boolean_query(query)
        #elapsed_time = time.time_ns() - start_time  # Calculate elapsed time
        query_timings[query] = elapsed_time
    except TimeoutError:
        query_timings[query] = "Timeout"


# Calculate average, maximum, and minimum timings
query_times = list(query_timings.values())
avg_time = sum(query_times) / len(query_times)
max_time = max(query_times)
min_time = min(query_times)
print("Net time = ")
print(sum(query_times))

# Print query timings
print("Query Timings (Boolean Retrieval Model):")
for query, timing in query_timings.items():
    print(f"{query}: {timing} seconds")

print(f"Average Time: {avg_time} seconds")
print(f"Maximum Time: {max_time} seconds")
print(f"Minimum Time: {min_time} seconds")



def profile_queries():
    pr = cProfile.Profile()
    pr.enable()
    for query_info in queries:
        query = query_info['query']
        try:
            execute_boolean_query(query)
        except TimeoutError:
            pass
    pr.disable()
    # Print profiling results
    ps = pstats.Stats(pr)
    ps.print_stats()

# Run the profiling
profile_queries()




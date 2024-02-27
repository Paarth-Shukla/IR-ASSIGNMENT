import json
import time
import os
import psutil

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
postings_file = 's2/intermediate/postings.tsv'
postings_dict = read_postings(postings_file)

# Function to execute boolean queries
def execute_boolean_query(query):
    start_time = time.time()  # Record start time
    query_terms = query.split()  # Split query into terms
    relevant_docs = set(postings_dict.get(query_terms[0], []))

    # Apply AND and OR operations
    for term in query_terms[1:]:
        if term.lower() == 'and':
            query_op = 'AND'
        elif term.lower() == 'or':
            query_op = 'OR'
        else:
            relevant_docs = set()  # Reset relevant_docs for the next term
            continue

        next_term_docs = set(postings_dict.get(query_terms[query_terms.index(term) + 1], []))
        if query_op == 'AND':
            relevant_docs &= next_term_docs
        elif query_op == 'OR':
            relevant_docs |= next_term_docs

    elapsed_time = time.time() - start_time  # Calculate elapsed time
    return elapsed_time

# Load queries
with open('s2/s2_query.json') as json_file:
    data = json.load(json_file)
queries = data['queries']

# Benchmark each query
for query_info in queries:
    query = query_info['query']
    
    # Benchmark grep
    grep_start_time = time.time()
    os.system(f"grep -rl \"{query}\" s2\s2_doc.json > /dev/null")
    grep_time = time.time() - grep_start_time

    # Benchmark boolean retrieval
    boolean_retrieval_time = execute_boolean_query(query)

    # Print results
    print(f"Query: {query}")
    print(f"  Grep Time: {grep_time:.8f} seconds")
    print(f"  Boolean Retrieval Time: {boolean_retrieval_time:.8f} seconds")
    print()

#Untested Code````````````````



import re
import time
import subprocess

# Sample inverted index (dictionary) containing terms and their posting lists
inverted_index = {
    'deep': [1, 3, 5],
    'learning': [2, 4, 5],
    # Add more terms and posting lists as needed
}

# Sample query file (s2/s2 query.json)
queries = [
    'deep learning',
    'information retrieval',
    # Add more queries from your file
]

def boolean_query(query):
    # Convert query to boolean format (e.g., "deep learning" -> "<deep AND learning>")
    boolean_query = ' AND '.join(query.split())
    return boolean_query

def execute_boolean_query(query):
    start_time = time.time()
    result = []
    for term in query.split(' AND '):
        if term in inverted_index:
            result.append(inverted_index[term])
    end_time = time.time()
    return result, end_time - start_time

def execute_grep_query(query):
    start_time = time.time()
    try:
        grep_output = subprocess.check_output(['grep', '^' + query, 'index-low.txt'], text=True)
        matched_documents = [int(line.split()[1]) for line in grep_output.strip().split('\n')]
    except subprocess.CalledProcessError:
        matched_documents = []
    end_time = time.time()
    return matched_documents, end_time - start_time

def main():
    for query in queries:
        boolean_query_str = boolean_query(query)
        
        # Execute boolean query using inverted index
        inverted_index_result, inverted_index_time = execute_boolean_query(boolean_query_str)
        print(f"Boolean Query: {boolean_query_str}")
        print(f"Inverted Index Result: {inverted_index_result}")
        print(f"Time taken (Inverted Index): {inverted_index_time:.6f} seconds\n")
        
        # Execute grep command
        grep_result, grep_time = execute_grep_query(query)
        print(f"Grep Query: {query}")
        print(f"Grep Result: {grep_result}")
        print(f"Time taken (grep): {grep_time:.6f} seconds\n")

if __name__ == "__main__":
    main()

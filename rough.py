from concurrent.futures import TimeoutError
import json
import time
import cProfile
import pstats



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
start_time = time.time()
postings_file = 's2/intermediate/postings.tsv'
postings_dict = read_postings(postings_file)
elapsed_time = time.time()-start_time
for key, value in postings_dict.items():
        print(key, ':', value)
print(elapsed_time)



# query_op = query_terms[i]  # Get the operator
#     term = query_terms[i + 1]  # Get the next term
#     next_term_docs = set(postings_dict.get(term, []))
#     if query_op.lower() == 'and':
#          relevant_docs &= next_term_docs
#     elif query_op.lower() == 'or':
#         relevant_docs |= next_term_docs

# import json

# # Load the JSON file
# with open('s2\s2_query.json') as f:
#     data = json.load(f)

# # Extract the queries into a list
# queries = [query_obj['query'] for query_obj in data['queries']]

# # Print the list of queries
# print(queries)

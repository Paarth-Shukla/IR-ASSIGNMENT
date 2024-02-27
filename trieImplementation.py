import json
import time
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

def load_queries(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return [query["query"] for query in data["queries"]]


#Reading the postings.tsv
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

postings_file = 's2/intermediate/postings.tsv'
postings_dict = read_postings(postings_file)

def perform_boolean_retrieval(queries, trie, postings_dict):
    timings = []
    for query in queries:
        start_time = time.time()
        # Perform boolean retrieval using the trie
        if trie.search(query):
            # Retrieve postings from postings_dict if query exists in trie
            postings_list = postings_dict.get(query, [])
        else:
            postings_list = []
        elapsed_time = time.time() - start_time
        timings.append(elapsed_time)
        print(f"Query: {query}, Postings: {postings_list}, Time: {elapsed_time:.8f} seconds")
    return timings


# Load queries from the JSON file
queries = load_queries("s2/s2_query.json")

# Initialize trie-based dictionary
trie_dict = Trie()
for query in queries:
    trie_dict.insert(query)

# Perform boolean retrieval using trie-based dictionary
trie_timings = perform_boolean_retrieval(queries, trie_dict, postings_dict)


# Compare timings
avg_time_trie = sum(trie_timings) / len(trie_timings)
max_time_trie = max(trie_timings)
min_time_trie = min(trie_timings)

print("Trie-based Dictionary:")
print(f"Average Time: {avg_time_trie} seconds")
print(f"Maximum Time: {max_time_trie} seconds")
print(f"Minimum Time: {min_time_trie} seconds")

import json
import cProfile
import pstats
import io
import time
import sys

class Node:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.postings = set()

class ForwardIndex:
    def __init__(self):
        self.root = Node()

    def insert(self, term, doc_id):
        node = self.root
        for char in term:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_end_of_word = True
        node.postings.add(doc_id)

    def wildcard_query(self, prefix):
        prefix = prefix.lower()
        results = set()
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return set()
        self._traverse(node, prefix, results)
        return results

    def _traverse(self, node, prefix, results):
        if node.is_end_of_word:
            results.update(node.postings)
        for char, child_node in node.children.items():
            self._traverse(child_node, prefix + char, results)

class BackwardIndex:
    def __init__(self):
        self.root = Node()

    def insert(self, term, doc_id):
        node = self.root
        for char in reversed(term):
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_end_of_word = True
        node.postings.add(doc_id)

    def wildcard_query(self, prefix):
        prefix = prefix.lower()
        results = set()
        node = self.root
        for char in reversed(prefix):
            if char in node.children:
                node = node.children[char]
            else:
                return set()
        self._traverse(node, prefix, results)
        return results

    def _traverse(self, node, prefix, results):
        if node.is_end_of_word:
            results.update(node.postings)
        for char, child_node in node.children.items():
            self._traverse(child_node, prefix + char, results)

# Load wildcard queries from the JSON file
with open("s2\s2_wildcard.json") as json_file:
    wildcard_data = json.load(json_file)

wildcard_queries = [query["query"] for query in wildcard_data["queries"]]

# Construct forward and backward tree-based indexes
forward_index = ForwardIndex()
backward_index = BackwardIndex()
for query in wildcard_queries:
    terms = query.split()
    for term in terms:
        forward_index.insert(term, query)
        backward_index.insert(term, query)

# Perform wildcard queries, measure time taken, and calculate memory consumed
query_timings = []
for query in wildcard_queries:
    start_time = time.time()
    forward_results = forward_index.wildcard_query("na")
    backward_results = backward_index.wildcard_query("la")
    results = forward_results.intersection(backward_results)
    elapsed_time = time.time() - start_time
    query_timings.append(elapsed_time)
    print(f"Query: {query}, Results: {results}, Time: {elapsed_time} seconds")

# Calculate minimum, maximum, and average time taken per query
min_time = min(query_timings)
max_time = max(query_timings)
avg_time = sum(query_timings) / len(query_timings)

# Calculate memory consumed by the indexes
forward_index_memory = sys.getsizeof(forward_index)
backward_index_memory = sys.getsizeof(backward_index)

print("\nPerformance Metrics:")
print(f"Minimum Time per Query: {min_time} seconds")
print(f"Maximum Time per Query: {max_time} seconds")
print(f"Average Time per Query: {avg_time} seconds")

print("\nMemory Consumed by the Indexes:")
print(f"Forward Index Memory: {forward_index_memory} bytes")
print(f"Backward Index Memory: {backward_index_memory} bytes")

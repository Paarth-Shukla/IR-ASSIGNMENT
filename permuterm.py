import json
import sys
import time

class PermutermIndex:
    def __init__(self):
        self.index = {}

    def add_term(self, term):
        term = term.lower()  # Convert term to lowercase
        term += '$'  # Add a special character to mark the end of the term
        for i in range(len(term)):
            rotated_term = term[i:] + term[:i]  # Generate permuterm by rotating the term
            self.index.setdefault(rotated_term, []).append(term[:-1])  # Remove the special character from the rotated term

    def construct_index(self, terms):
        for term in terms:
            self.add_term(term)

    def wildcard_query(self, query):
        query = query.lower()  # Convert query to lowercase
        query += '*'  # Add a special character to mark the end of the query
        results = set()
        for i in range(len(query)):
            rotated_query = query[i:] + query[:i]  # Generate permuterm for the query
            if rotated_query in self.index:
                results.update(self.index[rotated_query])  # Add matching terms to the results set
        return list(results)

    def prefix_search(self, prefix):
        prefix = prefix.lower()
        results = set()
        for key in self.index.keys():
            if key.startswith(prefix):
                results.update(self.index[key])
        return list(results)

# Load wildcard queries from the JSON file
with open(r"s2\s2_wildcard.json") as json_file:
    wildcard_data = json.load(json_file)

wildcard_queries = [query["query"] for query in wildcard_data["queries"]]

# Construct Permuterm index
permuterm_index = PermutermIndex()
permuterm_index.construct_index(wildcard_queries)

# Perform prefix-based search for each query and note the time taken per query
query_timings = []
for query in wildcard_queries:
    start_time = time.time()
    results = permuterm_index.prefix_search(query)
    elapsed_time = time.time() - start_time
    query_timings.append(elapsed_time)
    print(f"Query: {query}, Results: {results}, Time: {elapsed_time} seconds")

# Calculate minimum, maximum, and average time taken per query
min_time = min(query_timings)
max_time = max(query_timings)
avg_time = sum(query_timings) / len(query_timings)

print("\nPerformance Metrics:")
print(f"Minimum Time per Query: {min_time} seconds")
print(f"Maximum Time per Query: {max_time} seconds")
print(f"Average Time per Query: {avg_time} seconds")

# Note the memory consumed by the index
memory_consumed = sys.getsizeof(permuterm_index.index)
print(f"\nMemory Consumed by the Index: {memory_consumed} bytes")

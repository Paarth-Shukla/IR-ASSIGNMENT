import json
import cProfile
import pstats
import io

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

# Profile the execution of each query
for query in wildcard_queries:
    profiler = cProfile.Profile()
    profiler.enable()
    results = permuterm_index.prefix_search(query)
    profiler.disable()
    
    # Output profiling results
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats()
    
    print(f"Query: {query}, Results: {results}")
    print(stream.getvalue())

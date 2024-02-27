import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')

# Load the JSON data
with open(r's2/s2_query.json') as json_file:
    data = json.load(json_file)
queries = data['queries']

# Extract individual query terms
query_terms = []
for query_info in queries:
    query = query_info['query']
    terms = query.split()
    query_terms.extend(terms)

# Sort the query terms in ascending order
query_terms.sort()

def preprocess_vocabulary(vocabulary):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    stemmed_vocabulary = []
    for word in vocabulary:
        # Tokenize the word
        tokens = word_tokenize(word)
        # Stemming
        stemmed_words = [stemmer.stem(token) for token in tokens]
        # Remove stop words
        filtered_words = [word for word in stemmed_words if word.lower() not in stop_words]
        # Join the tokens back to a single word
        processed_word = ' '.join(filtered_words)
        stemmed_vocabulary.append(processed_word)
    
    return stemmed_vocabulary

# Assuming 'vocabulary' is a list of words
stemmed_terms = preprocess_vocabulary(query_terms)

# Print the stemmed terms
for term in stemmed_terms:
    print(term)

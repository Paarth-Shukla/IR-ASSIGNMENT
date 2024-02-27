import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the JSON data
with open(r's2/s2_doc.json') as json_file:
    data = json.load(json_file)
papers = data['all_papers']

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Open a file for writing with UTF-8 encoding
with open(r'testing\lemmatized_words.txt', 'w', encoding='utf-8') as f:
    for paper in papers:
        abstracts = paper['paperAbstract']
        for abstract in abstracts:
            # Tokenize the abstract
            tokens = word_tokenize(abstract)
            # Remove stop words
            filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
            # Lemmatize the remaining words
            lemmatized_words = [lemmatizer.lemmatize(token) for token in filtered_tokens]
            # Write the lemmatized words to the file
            f.write(' '.join(lemmatized_words) + '\n')

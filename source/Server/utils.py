import hashlib
from settings import LOGSIZE
import nltk as nl
from nltk.corpus import stopwords
import unicodedata
import re
import inflect
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def hash(message):
    digest = hashlib.sha256(message.encode()).hexdigest()
    digest = int(digest, 16) % pow(2, LOGSIZE)
    return digest

def _tokenize_text(text):
    return nl.word_tokenize(text)

def _remove_non_ascii(text):
    new_text = []
    for w in text:
        new_word = unicodedata.normalize('NFKD', w).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_text.append(new_word)
    
    return new_text

def _to_lower(text):
    return [w.lower() for w in text]

def _remove_stopwords(text):
    new_text = []
    for w in text:
        if w not in stopwords.words('english'):
            new_text.append(w)
        
    return new_text

def _remove_puntuation(text):
    new_text = []
    for w in text:
        new_word = re.sub(r'[^\w\s]', '', w)
        new_text.append(new_word) if new_word != '' else None
    
    return new_text

def _replace_numbers(text):
    p = inflect.engine()
    new_text = []
    
    for w in text:
        if w.isdigit():
            try:
                w = p.number_to_words(w)
                w = w.replace('and', '')
                w = w.replace('-', ' ')
                
                for word in w.split():
                    new_text.append(word)
            except:
                pass
        else:
            new_text.append(w)
    
    return new_text

def _stemm_text(text):
    ps = nl.PorterStemmer()
    stemms = []
    for w in text:
        stemms.append(ps.stem(w))

    return stemms

def process_text(string_format):
    text = _tokenize_text(string_format)
    text = _remove_non_ascii(text)
    text = _to_lower(text)
    text = _remove_stopwords(text)
    text = _remove_puntuation(text)
    text = _replace_numbers(text)
    text = _stemm_text(text)
    
    return " ".join(text)

def get_similarity(text_1, text_2):
    text_1 = process_text(text_1)
    text_2 = process_text(text_2)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([text_1, text_2])
    similarity_matrix = cosine_similarity(X, X)
    return similarity_matrix[0][1]
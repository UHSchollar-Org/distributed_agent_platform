import hashlib
from settings import LOGSIZE
import nltk as nl
from nltk.corpus import stopwords
import unicodedata
import re
import inflect

def hash(message):
    digest = hashlib.sha256(message.encode()).hexdigest()
    digest = int(digest, 16) % pow(2, LOGSIZE)
    return digest

def tokenize_text(text):
    return nl.word_tokenize(text)

def remove_non_ascii(text):
    new_text = []
    for w in text:
        new_word = unicodedata.normalize('NFKD', w).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_text.append(new_word)
    
    return new_text

def to_lower(text):
    return [w.lower() for w in text]

def remove_stopwords(text):
    new_text = []
    for w in text:
        if w not in stopwords.words('english'):
            new_text.append(w)
        
    return new_text

def remove_puntuation(text):
    new_text = []
    for w in text:
        new_word = re.sub(r'[^\w\s]', '', w)
        new_text.append(new_word) if new_word != '' else None
    
    return new_text

def replace_numbers(text):
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

def stemm_text(text):
    ps = nl.PorterStemmer()
    stemms = []
    for w in text:
        stemms.append(ps.stem(w))

    return stemms
    
def process_text(string_format):
    text = tokenize_text(string_format)
    text = remove_non_ascii(text)
    text = to_lower(text)
    text = remove_stopwords(text)
    text = remove_puntuation(text)
    text = replace_numbers(text)
    text = stemm_text(text)
    return text
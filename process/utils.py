import re

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import string
from collections import Counter
import requests

def clean_english_text(text):
    pattern = r"[^a-zA-Z0-9\s\.,!?;:'\"()\-–—&@#$%^*/+=<>\[\]{}]"
    
    cleaned_text = re.sub(pattern, "", text)
    
    return cleaned_text

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)

    lemmatized_words = []
    for word, pos in pos_tags:
        if word in string.punctuation:
            continue
            
        wordnet_pos = get_wordnet_pos(pos)
        
        lemma = lemmatizer.lemmatize(word, pos=wordnet_pos)
        lemmatized_words.append(lemma)
    
    return ' '.join(lemmatized_words)

def frequency_similarity(s1, s2):
    if not s1 and not s2:
        return 1.0
    
    counter1 = Counter(s1)
    counter2 = Counter(s2)
    
    all_chars = set(counter1.keys()).union(set(counter2.keys()))
    if not all_chars:  # 如果两个字符串都是空字符串
        return 1.0
    
    common_chars = 0
    for char in all_chars:
        if counter1[char] == counter2[char]:
            common_chars += 1
    
    return common_chars / len(all_chars)

def can_transform_by_spaces(s1, s2):
    return s1.replace(' ', '') == s2.replace(' ', '')

def deduplicate_content(content_container):
    content_list = sorted(content_container)
    similarity_score = []
    for i in range(len(content_list)-1):
        similarity_score.append(frequency_similarity(content_list[i], content_list[i+1]))
    conflict_idx = [idx for idx, item in enumerate(similarity_score) if item > 0.8]
    delete_idxs = []
    for i in conflict_idx:
        if can_transform_by_spaces(content_list[i], content_list[i+1]):
            delete_idxs.insert(0,i)
    
    for idx in delete_idxs:
        del content_list[idx]
    return content_list

def query(dataset_name, text):
    url = "http://127.0.0.1:8000/retrieve/"
    params = {
        "corpus_name": dataset_name,
        "query_text": text,
    }
    return requests.post(url, json=params, proxies={'all': None})

def can_transform_by_spaces(s1, s2):
    return s1.replace(' ', '') == s2.replace(' ', '')
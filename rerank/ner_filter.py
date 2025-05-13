from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from diskcache import Cache
import os
import spacy

os.makedirs("./rerank/cache", exist_ok=True)
cache = Cache("./rerank/cache")

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")
bert_nlp = pipeline("ner", model=model, tokenizer=tokenizer)
spacy_nlp = spacy.load("en_core_web_sm")

stop_words = {"what", "is", "the", "of", "to", "and", "in", 
                "for", "on", "with", "at", "from", "by", "about", 
                "as", "into", "like", "through", "after", "over", 
                "between", "out", "against", "during", 
                "without", "before", "under", "around", 
                "among", "but", "or", "nor", "because", 
                "if", "while", "until", "unless", "since", 
                "although", "though", "who", "whom", "whose", 
                "which", "that", "this", "these", "those", "am", 
                "are", "was", "were", "be", "been", "being", "have", "has", 
                "had", "having", "do", "does", "did", "doing", "a", "an", "the", 
                "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", 
                "by", "for", "with", "about", "against", "between", "into", "through", 
                "during", "before", "after", "above", "below", "to", "from", "up", 
                "down", "in", "out", "on", "off", "over", "under", "again", "further", 
                "then", "once", "here", "there", "when", "where", "why", "how", "all", 
                "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", 
                "nor", "not", "only", "own", "same", "so", "than", "too", "very", 
                "can", "will", "just", "don", "should", "now"}

# @cache.memoize()
def bert_extract_entity(text):
    subwords = [item['word'] for item in bert_nlp(text)]


    merged_words = []
    current_word = ""
    for subword in subwords:
        if subword.startswith("##"):
            current_word += subword[2:]
        else:
            if current_word:
                merged_words.append(current_word)
            current_word = subword
    if current_word:
        merged_words.append(current_word)
    final_merged_words = []
    i = 0
    while i < len(merged_words):
        word = merged_words[i]
        if i + 2 < len(merged_words):
            next_word = merged_words[i + 2]
            combined_word = word + merged_words[i + 1] + next_word
            if combined_word in text:
                final_merged_words.append(combined_word)
                i += 3
            else:
                final_merged_words.append(word)
                i += 1
        else:
            final_merged_words.append(word)
            i += 1
    final_merged_words = [word for word in final_merged_words if word.lower() not in stop_words]
    final_merged_words = set(final_merged_words)
    return final_merged_words

# @cache.memoize()
def spacy_extract_nouns(text):
    doc =spacy_nlp(text)
    
    nouns = []
    for chunk in doc.noun_chunks:
        if " " not in chunk.text:
            nouns.append(chunk.text)
    nouns.extend(token.text for token in doc if token.pos_ == "NOUN" and " " not in token.text)
    return set(nouns)

def ner_wrapper(text):
    result = bert_extract_entity(text)
    if not result:
        result = spacy_extract_nouns(text)
    return result

def ner_filter(thought, retrieved_documents, question=None):
    query_entity = ner_wrapper(thought)
    if question:
        query_entity |= ner_wrapper(question)
    result = []
    result_id = []
    for doc in retrieved_documents:
        is_valid = False
        # doc_entity = set(bert_extract_entity(doc['paragraph_text']))
        for word in query_entity:
            if word in doc['paragraph_text']:
                is_valid = True
                break
        if is_valid:
            result.append(doc)
            result_id.append(doc['id'])
    return result, result_id
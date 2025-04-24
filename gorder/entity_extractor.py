from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from diskcache import Cache
import os
import spacy

os.makedirs("./gorder/cache", exist_ok=True)
cache = Cache("./gorder/cache")

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")
bert_nlp = pipeline("ner", model=model, tokenizer=tokenizer)

spacy_nlp = spacy.load("en_core_web_sm")


def bert_entity_extractor(text):
    ner_results = bert_nlp(text)
    return [item['word'] for item in ner_results]


def spacy_extract_nouns(text):
    doc = spacy_nlp(text)
    
    nouns = []
    for chunk in doc.noun_chunks:
        nouns.append(chunk.text)
    nouns.extend(token.text for token in doc if token.pos_ == "NOUN")
    return list(set(nouns))

@cache.memoize()
def entity_extractor(text):
    combined_entities = set(bert_entity_extractor(text)) | set(spacy_extract_nouns(text))
    return list(combined_entities)
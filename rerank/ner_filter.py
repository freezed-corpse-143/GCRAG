from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from diskcache import Cache
import os

os.makedirs("./rerank/cache", exist_ok=True)
cache = Cache("./rerank/cache")

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")
bert_nlp = pipeline("ner", model=model, tokenizer=tokenizer)

@cache.memoize()
def bert_entity_extractor(text):
    ner_results = bert_nlp(text)
    return [item['word'] for item in ner_results]


def ner_filter(question, retrieved_documents, thought):
    quetion_entity = set(bert_entity_extractor(question))
    thought_entity = set(bert_entity_extractor(thought))
    query_entity = quetion_entity | thought_entity
    result = []
    result_id = []
    for doc in retrieved_documents:
        doc_entity = set(bert_entity_extractor(doc['paragraph_text']))
        if len(doc_entity & query_entity) != 0:
            result.append(doc)
            result_id.append(doc['id'])
    return result, result_id
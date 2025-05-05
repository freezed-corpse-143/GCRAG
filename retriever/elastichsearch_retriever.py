from elasticsearch import Elasticsearch
from diskcache import Cache
import os
from typing import List, Dict
from collections import OrderedDict

os.makedirs("./retriever/cache/elasticsearch_cache", exist_ok=True)

cache = Cache("./retriever/elasticsearch_cache")

retriever = Elasticsearch(["localhost"], scheme="http", port=9200, timeout=30)

CORPUS_NAME = os.environ['CORPUS_NAME']

def retrieve_from_elasticsearch(
    query_text: str,
    max_hits_count: int = 25,
) -> List[Dict]:
    return _retrieve(CORPUS_NAME, query_text, max_hits_count)
    

@cache.memoize()
def _retrieve(
    corpus_name: str,
    query_text: str,
    max_hits_count: int = 25,
) -> List[Dict]:
    query = {
        "size": max_hits_count,
        # what records are needed in result
        "_source": ["id", "paragraph_text"],
        "query": {
            "bool": {
                "should": [],
            }
        },
    }

    query["query"]["bool"]["should"].append({"match": {"paragraph_text": query_text}})

    result = retriever.search(index=corpus_name, body=query)

    retrieval = []
    if result.get("hits") is not None and result["hits"].get("hits") is not None:
        retrieval = result["hits"]["hits"]
        text2retrieval = OrderedDict()
        for item in retrieval:
            text = item["_source"]["paragraph_text"].strip().lower()
            text2retrieval[text] = item
        retrieval = list(text2retrieval.values())

    retrieval = sorted(retrieval, key=lambda e: e["_score"], reverse=True)
    retrieval = retrieval[:max_hits_count]
    for retrieval_ in retrieval:
        retrieval_["_source"]["score"] = retrieval_["_score"]
    retrieval = [e["_source"] for e in retrieval]

    for retrieval_ in retrieval:
        retrieval_["corpus_name"] = corpus_name

    return retrieval

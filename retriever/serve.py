from time import perf_counter
from fastapi import FastAPI, Request
from elasticsearch import Elasticsearch
from typing import List, Dict
from collections import OrderedDict
from diskcache import Cache
import os

os.makedirs("./retriever/cache", exist_ok=True)

cache = Cache("./retriever/cache")

retriever = Elasticsearch(["localhost"], scheme="http", port=9200, timeout=30)

@cache.memoize()
def retrieve_from_elasticsearch(
    corpus_name: str,
    query_text: str,
    max_buffer_count: int = 100,
    max_hits_count: int = 10,
) -> List[Dict]:

    query = {
        "size": max_buffer_count,
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

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello! This is a retriever server."}


@app.post("/retrieve/")
async def retrieve(arguments: Request):  # see the corresponding method in unified_retriever.py
    arguments = await arguments.json()
    start_time = perf_counter()
    retrieval = retrieve_from_elasticsearch(**arguments)
    end_time = perf_counter()
    time_in_seconds = round(end_time - start_time, 1)
    return {"retrieval": retrieval, "time_in_seconds": time_in_seconds}
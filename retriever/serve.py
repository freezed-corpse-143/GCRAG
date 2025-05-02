from time import perf_counter
from fastapi import FastAPI, Request

import os

RETRIEVAL_METHOD = os.environ["RETRIEVAL_METHOD"]
if RETRIEVAL_METHOD == "elasticsearch":
    from elastichsearch_retriever import retrieve_from_elasticsearch as retrieve
elif RETRIEVAL_METHOD == "colbert":
    from colbert_retriever import retrieve_from_colbert as retrieve



app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello! This is a retriever server."}


@app.post("/retrieve/")
async def retrieve(arguments: Request):  # see the corresponding method in unified_retriever.py
    arguments = await arguments.json()
    start_time = perf_counter()
    retrieval = retrieve(**arguments)
    end_time = perf_counter()
    time_in_seconds = round(end_time - start_time, 1)
    return {"retrieval": retrieval, "time_in_seconds": time_in_seconds}
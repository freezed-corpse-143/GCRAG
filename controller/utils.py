import requests

retrieval_url = "http://127.0.0.1:8000/retrieve/"
generate_url = "http://127.0.0.1:8010/generate/"

def retrieve(corpus_name: str, query_text: str):
    params = {
        "corpus_name": corpus_name,
        "query_text": query_text,
    }
    response = requests.post(retrieval_url, json=params, proxies={"http": None, "https": None, "all": None})
    return response.json()


def generate(prompt):
    params = {"prompt": prompt}
    response = requests.get(generate_url, params=params, proxies={"http": None, "https": None, "all": None})
    return response.json()


def format_retrieved_documents(retrieved_documents):
    output = ""
    for idx, item in enumerate(retrieved_documents):
        output += f"evidence {idx+1}:\n{item['paragraph_text']}"
    return output.strip()


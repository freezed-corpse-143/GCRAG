import requests

retrieval_url = "http://127.0.0.1:8000/retrieve/"
generate_url = "http://127.0.0.1:8010/generate/"

def retrieve(query_text: str):
    params = {
        "query_text": query_text,
    }
    response = requests.post(retrieval_url, json=params, proxies={"http": None, "https": None, "all": None})
    return response.json()


def generate(prompt , stop = None):
    params = {"prompt": prompt}
    if stop:
        params['stop'] = stop
    response = requests.post(generate_url, json=params, proxies={"http": None, "https": None, "all": None})
    return response.json()
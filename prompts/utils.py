import requests

generate_url = "http://127.0.0.1:8010/generate/"

def generate(prompt):
    params = {"prompt": prompt}
    response = requests.get(generate_url, params=params, proxies={"http": None, "https": None, "all": None})
    return response.json()
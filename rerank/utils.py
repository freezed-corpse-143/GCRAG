import requests
import re

generate_url = "http://127.0.0.1:8010/generate/"

def format_retr_docs(retr_docs):
    result = ""
    for idx, d in enumerate(retr_docs):
        result += f"Document {idx+1}: " + d['paragraph_text'] + "\n"
    return result.strip()

def generate(prompt):
    params = {"prompt": prompt}
    response = requests.get(generate_url, params=params, proxies={"http": None, "https": None, "all": None})
    return response.json()

def extract_from_ground_answer(text):
    new_answer_match = re.search(r'New answer:(.*?)(?=supporting fact ids:|$)', text, re.DOTALL)
    new_answer = new_answer_match.group(1).strip() if new_answer_match else None
    
    fact_ids_match = re.search(r'Supporting fact ids:(.*?)(?=$)', text)
    fact_ids_str = fact_ids_match.group(1).strip() if fact_ids_match else ""
    
    fact_ids = [int(num) for num in re.findall(r'[1-9]', fact_ids_str)] if fact_ids_str else []
    return (new_answer, fact_ids)
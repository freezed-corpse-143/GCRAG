import requests
import re
import json

retrieval_url = "http://127.0.0.1:8000/retrieve/"
generate_url = "http://127.0.0.1:8010/generate/"

def retrieve(query_text: str):
    params = {
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

def extract_thought_answer(text):
    # Pattern that matches both numbered and unnumbered Thought/Answer pairs
    pattern = r"Thought(?:\s*(\d+))?: (.*?)\nAnswer(?:\s*\1)?: (.*?)(?=\nThought(?:\s*\d+)?:|$)"
    result = []
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        thought_num, thought, answer = matches[0]
        result.append(thought.replace("\n"," ").strip())
        result.append(answer.replace("\n", " ").strip())
    return result

def extract_answer(input_string):
    # print(input_string)
    match = re.search(r'FINISH\[(.*?)\]', input_string)
    if match:
        return match.group(1)
    else:
        return "Unknown"


def parse_json(text, max_attempts = 3):
    attempts = 0
    last_error = None
    
    while attempts < max_attempts:
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            last_error = e
            attempts += 1
            if attempts < max_attempts:
                prompt = f"Convert the following text to standard JSON format. Return ONLY the JSON content without any additional explanations or comments:\n\n{text}"
                try:
                    generated = generate(prompt)['generated_text']
                    if isinstance(generated, dict):
                        text = json.dumps(generated)
                    else:
                        text = str(generated)
                except Exception as e:
                    last_error = e
    

    raise ValueError(f"Failed to parse JSON after {max_attempts} attempts. Last error: {str(last_error)}")

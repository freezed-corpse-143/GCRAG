import requests
import re
from collections import Counter

generate_url = "http://127.0.0.1:8010/generate/"

def format_retr_docs(retr_docs):
    result = ""
    for idx, d in enumerate(retr_docs):
        result += f"Document {idx+1}: " + d['paragraph_text'] + "\n"
    return result.strip()

def generate(prompt, stop=None):
    params = {"prompt": prompt}
    if stop:
        params['stop'] = stop
    response = requests.post(generate_url, json=params, proxies={"http": None, "https": None, "all": None})
    return response.json()

def extract_from_ground_answer(text):
    # new_answer_match = re.search(r'New answer:(.*?)(?=supporting fact ids:|$)', text, re.DOTALL)
    new_answer_match = re.search(r'New answer:(.*?)(?=$)', text, re.DOTALL)
    new_answer = new_answer_match.group(1).strip() if new_answer_match else None
    
    # fact_ids_match = re.search(r'Supporting fact ids:(.*?)(?=$)', text)
    # fact_ids_str = fact_ids_match.group(1).strip() if fact_ids_match else ""
    
    # fact_ids = [int(num) for num in re.findall(r'[1-9]', fact_ids_str)] if fact_ids_str else []
    # return (new_answer, fact_ids)
    return new_answer

re_art = re.compile(r'\b(a|an|the)\b')
re_punc = re.compile(r'[!"#$%&()*+,-./:;<=>?@\[\]\\^`{|}~_\']')

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re_art.sub(' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        return re_punc.sub(' ', text)  # convert punctuation to spaces

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def _prec_recall_f1_score(pred_items, gold_items):
    """
    Compute precision, recall and f1 given a set of gold and prediction items.

    :param pred_items: iterable of predicted values
    :param gold_items: iterable of gold values

    :return: tuple (p, r, f1) for precision, recall, f1
    """
    common = Counter(gold_items) & Counter(pred_items)
    num_same = sum(common.values())
    if num_same == 0:
        return 0, 0, 0
    precision = 1.0 * num_same / len(pred_items)
    recall = 1.0 * num_same / len(gold_items)
    f1 = (2 * precision * recall) / (precision + recall)
    return precision, recall, f1

def single_f1_score(guess, answers):
    if guess is None or answers is None:
        return 0
    g_tokens = normalize_answer(guess).split()
    scores = [
        _prec_recall_f1_score(g_tokens, normalize_answer(a).split()) for a in answers
    ]
    return [f1 for p, r, f1 in scores]
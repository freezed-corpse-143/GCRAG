import jsonlines
import os
import ujson
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_row(row, qid_aliases):
    """Process a single row to format it."""
    
    answer_object = [row["answer"]]
    answer_id = row['answer_id']
    if answer_id :
        aliases =  qid_aliases[answer_id]
        if aliases:
            answer_object += aliases

    title_para = dict()
    for item in row["context"]:
        title = item[0]
        title_para[title] = item[1]

    sp_title_snippets = dict()
    for item in row["supporting_facts"]:
        title = item[0]
        if title not in sp_title_snippets:
            sp_title_snippets[title] = []
        try:
            para = title_para[title][item[1]]
            sp_title_snippets[title].append(para)
        except Exception as e:
            pass

    return {
        "id": row["_id"],
        "question": row["question"],
        "answer": answer_object,
        "context": [{
            "title": item[0], 
            "content": ' '.join(item[1]).replace('\xa0', ' ').replace("  ", " "),
            "sp_snippets": sp_title_snippets[item[0]] if item[0] in sp_title_snippets else [],
            'is_supporting': item[0] in sp_title_snippets, }
            for item in row["context"]],
        "type": row["type"],
        "evidences": [
            {
                "fact": evidence[0],
                "relation": evidence[1],
                "entity": evidence[2],
            }
            for evidence in row["evidences"]
        ],
    }
def format_2wikimultihopqa(input_path, output_path, max_workers=12):
    """Process 2WikiMultihopQA data with parallel processing and unified writing."""
    data = ujson.load(open(input_path))
    with jsonlines.open('./download/2wikimultihopqa/id_aliases.json') as reader:
        aliases_data = list(reader)
    qid_aliases = dict()
    for row in aliases_data:
        qid_aliases[row['Q_id']] = row['aliases']
    
    # Process rows in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_row, row, qid_aliases) for row in data]
        
        with open(output_path, "w", encoding="utf-8") as f:
            for future in tqdm(as_completed(futures), total=len(data)):
                processed_item = future.result()
                f.write(ujson.dumps(processed_item, ensure_ascii=False) + "\n")

if __name__  == "__main__":
    os.makedirs("./datasets/2wikimultihopqa", exist_ok=True)
    format_2wikimultihopqa("./download/2wikimultihopqa/train.json", 
                           "./datasets/2wikimultihopqa/train.jsonl")
    format_2wikimultihopqa("./download/2wikimultihopqa/dev.json", 
                           "./datasets/2wikimultihopqa/dev.jsonl")
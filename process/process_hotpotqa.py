import ujson
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_example(example):
    """Process a single example to format it."""
    for k in ["answer", "type", "level"]:
        if k not in example.keys():
            example[k] = None
    if "supporting_facts" not in example.keys():
        example["supporting_facts"] = []

    
    
    title_para = dict()
    for item in example["context"]:
        title = item[0]
        title_para[title] = item[1]

    sp_title_snippets = dict()
    for item in example["supporting_facts"]:
        title = item[0]
        if title not in sp_title_snippets:
            sp_title_snippets[title] = []
        try:
            para = title_para[title][item[1]]
            sp_title_snippets[title].append(para)
        except Exception as e:
            pass
    
    
    return {  
        "id": example["_id"],
        "question": example["question"],
        "answer": [example["answer"]],
        "context": [{
            "title": f[0], 
            "content": " ".join(f[1]).strip().replace('\xa0', ' ').replace("  ", " "),
            "sp_snippets": sp_title_snippets[f[0]] if f[0] in sp_title_snippets else [],
            'is_supporting': f[0] in sp_title_snippets, } 
            for f in example["context"]],
        "type": example["type"],
        "level": example["level"],
    }

def format_hotpotqa(input_path, output_path, max_workers=12):
    """Process HotpotQA data with parallel processing and unified writing."""
    data = ujson.load(open(input_path))
    
    # Process examples in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_example, example) for example in data]
        
        # Write results as they become available
        with open(output_path, "w", encoding="utf-8") as f:
            for future in tqdm(as_completed(futures), total=len(data)):
                processed_item = future.result()
                f.write(ujson.dumps(processed_item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    os.makedirs("./datasets/hotpotqa", exist_ok=True)
    format_hotpotqa("./download/hotpotqa/hotpot_dev_distractor_v1.json", 
                    "./datasets/hotpotqa/dev.jsonl")
    format_hotpotqa("./download/hotpotqa/hotpot_train_v1.1.json", 
                    "./datasets/hotpotqa/train.jsonl")
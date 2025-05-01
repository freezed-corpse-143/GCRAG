import jsonlines
import json
from .utils import clean_text

def context_musique(jsonl_path_list):
    content_set = set()
    content_list = []
    for jsonl_path in jsonl_path_list:
        with jsonlines.open(jsonl_path) as reader:
            for row in reader:
                for para in row['paragraphs']:
                    content = para['paragraph_text'].strip().replace('\xa0', ' ').replace("  ", " ")
                    clean_content = clean_text(content)
                    if clean_content not in content_set:
                        content_set.add(clean_content)
                        content_list.append(content)

    with open("./datasets/musique/context.json", 'w') as f:
        json.dump(content_list, f, ensure_ascii=False)

if __name__ == "__main__":
    jsonl_path_list = [
        "./download/musique/musique_full_v1.0_train.jsonl",
        "./download/musique/musique_full_v1.0_dev.jsonl",
        "./download/musique/musique_full_v1.0_test.jsonl",
        "./download/musique/musique_ans_v1.0_train.jsonl",
        "./download/musique/musique_ans_v1.0_dev.jsonl",
        "./download/musique/musique_ans_v1.0_test.jsonl",
    ]

    context_musique(jsonl_path_list)
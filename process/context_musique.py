import jsonlines
import json
from .utils import deduplicate_content

def context_musique(jsonl_path_list):
    content_set = set()
    context = []
    for jsonl_path in jsonl_path_list:
        with jsonlines.open(jsonl_path) as reader:
            for row in reader:
                for para in row['paragraphs']:
                    content = para['paragraph_text'].replace('\xa0', ' ')
                    content_set.add(content)
                    context.append(content)
    with open("./datasets/musique/context.json", 'w') as f:
        json.dump(deduplicate_content(content_set), f, ensure_ascii=False)

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
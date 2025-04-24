import json
from .utils import deduplicate_content


def context_2wikimultihopqa(json_path_list):
    content_set = set()
    for json_path in json_path_list:
        data = json.load(open(json_path))
        for row in data:
            for para in row['context']:
                content = " ".join(para[1]).strip().replace('\xa0', ' ').replace("  ", " ")
                content_set.add(content)  

    with open("./datasets/2wikimultihopqa/context.json", 'w') as f:
        json.dump(deduplicate_content(content_set), f, ensure_ascii=False)

if __name__ == "__main__":
    json_path_list = [
        "./download/2wikimultihopqa/train.json",
        "./download/2wikimultihopqa/dev.json",
        "./download/2wikimultihopqa/test.json",
    ]
    context_2wikimultihopqa(json_path_list)
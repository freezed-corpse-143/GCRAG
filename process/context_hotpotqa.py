import json

def context_hotpotqa(json_path_list):
    content_set = set()
    for json_path in json_path_list:
        data = json.load(open(json_path))
        for row in data:
            for para in row['context']:
                content = " ".join(para[1]).strip().replace('\xa0', ' ')
                content_set.add(content)
    with open("./datasets/hotpotqa/context.json", 'w') as f:
        json.dump(list(content_set), f, ensure_ascii=False)

if __name__ == "__main__":
    json_path_list = [
        "./download/hotpotqa/hotpot_train_v1.1.json",
        "./download/hotpotqa/hotpot_dev_distractor_v1.json",
        "./download/hotpotqa/hotpot_dev_fullwiki_v1.json",
    ]
    context_hotpotqa(json_path_list)

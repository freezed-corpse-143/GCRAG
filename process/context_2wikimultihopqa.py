import ujson
from .utils import clean_text


def context_2wikimultihopqa(json_path_list):
    content_set = set()
    content_list = []
    for json_path in json_path_list:
        data = ujson.load(open(json_path))
        for row in data:
            for para in row['context']:
                content = " ".join(para[1]).strip().replace('\xa0', ' ').replace("  ", " ")
                clean_content = clean_text(content)
                if clean_content not in content_set:
                    content_set.add(clean_content)
                    content_list.append(content)

    with open("./datasets/2wikimultihopqa/context.json", 'w') as f:
        ujson.dump(content_list, f, ensure_ascii=False)

    tsv_item_list = []
    for idx, item in enumerate(content_list):
        clean_item = item.replace("\n", " ")
        tsv_item_list.append(
            f"{idx}\t{clean_item}"
        )

    with open(f"../datasets/2wikimultihopqa/context.tsv", "w") as f:
        f.write("\n".join(tsv_item_list))

if __name__ == "__main__":
    json_path_list = [
        "./download/2wikimultihopqa/train.json",
        "./download/2wikimultihopqa/dev.json",
        "./download/2wikimultihopqa/test.json",
    ]
    context_2wikimultihopqa(json_path_list)
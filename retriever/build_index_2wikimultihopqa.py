from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
import hashlib
from tqdm import tqdm

def calculate_32id_str(text):
    md5_hash = hashlib.md5(text.encode('utf-8'))
    return md5_hash.hexdigest()

def make_documents():
    documents = []
    data = json.load(open("./datasets/2wikimultihopqa/context.json"))
    id_set = set()
    for idx, para in enumerate(data):
        paragraph_id = calculate_32id_str(para)
        if paragraph_id not in id_set:
            id_set.add(paragraph_id)
        else:
            raise ValueError("id collision")
        documents.append({
            "_op_type": "create",
            "_index": "2wikimultihopqa",
            "_id": idx,
            "_source": {
                "id": paragraph_id,
                'paragraph_text': para,
            },
        })
    for document in tqdm(documents,  total=len(documents)):
        yield document


def main():
    es = Elasticsearch(
        [{"host": "localhost", "port": 9200}],
        max_retries=2,
        timeout=500,
        retry_on_timeout=True,
    )

    paragraphs_index_settings = {
        "mappings": {
            "properties": {
                "paragraph_text": {
                    "type": "text",
                    "analyzer": "english",
                },
            }
        }
    }
    elasticsearch_index = "2wikimultihopqa"
    index_exists = es.indices.exists(index=elasticsearch_index)

    if index_exists:
        es.indices.delete(index=elasticsearch_index)

    es.indices.create(index=elasticsearch_index, ignore=400, **paragraphs_index_settings)

    result = bulk(
        es,
        make_documents(),
        raise_on_error=True,
        raise_on_exception=True,
        max_retries=2,
        request_timeout=500,
    )
    es.indices.refresh(elasticsearch_index)
    document_count = result[0]
    print(f"Index {elasticsearch_index} is ready. Added {document_count} documents.")
    



if __name__ == "__main__":
    main()
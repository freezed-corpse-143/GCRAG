from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from tqdm import tqdm

def pad_to_32_bits(s):
    padding_length = 32 - len(s)
    if padding_length > 0:
        return '0' * padding_length + s
    else:
        return s[:32]

def make_documents():
    documents = []
    data = json.load(open("./datasets/hotpotqa/context.json"))
    for idx, para in enumerate(data):
        paragraph_id = pad_to_32_bits(str(idx))

        documents.append({
            "_op_type": "create",
            "_index": "hotpotqa",
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
    elasticsearch_index = "hotpotqa"
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
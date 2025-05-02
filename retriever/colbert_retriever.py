from diskcache import Cache
from colbert import Searcher
import os

os.makedirs("./retriever/cache/colbert_cache", exist_ok=True)

cache = Cache("./retriever/cache/colbert_cache")

CORPUS_NAME = os.environ['CORPUS_NAME']
INDEX_NAME = f"{CORPUS_NAME}.nbits=2"
root = os.path.abspath("./")
INDEX_ROOT = os.path.join(root, f"retriever/experiments/{CORPUS_NAME}/indexes")
searcher = Searcher(index=INDEX_NAME, 
                    index_root=INDEX_ROOT,
                    collection=os.path.join(root, f"datasets/{CORPUS_NAME}/context.tsv"))

def pad_to_32_bits(s):
    padding_length = 32 - len(s)
    if padding_length > 0:
        return '0' * padding_length + s
    else:
        return s[:32]

@cache.memoize()
def retrieve_from_colbert(query_text, max_hits_count=25):
    pids, ranks, scores = searcher.search(query_text, k=max_hits_count)
    retrieval = []
    for pid in pids:
        text = searcher.collection[pid]            
        d = {'paragraph_text': text, 'id': pad_to_32_bits(str(pid))}
        retrieval.append(d)
    return retrieval


from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Indexer
import argparse
import os

if __name__=='__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', help='Name of the dataset to index')
    args = parser.parse_args()
    root = os.path.abspath("./")
    dataset = args.dataset
    
    with Run().context(RunConfig(nranks=1, experiment=dataset)):
        config = ColBERTConfig(
            nbits=2,
            root=os.path.join(root, "retriever"),
        )
        indexer = Indexer(checkpoint="colbert-ir/colbertv2.0", config=config)
        indexer.index(name=f"{dataset}.nbits=2", collection=os.path.join(root, f"datasets/{dataset}/context.tsv"),
                      overwrite=True)

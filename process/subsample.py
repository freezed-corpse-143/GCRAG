import random
import jsonlines
from .utils import query, can_transform_by_spaces
import argparse
from tqdm import tqdm


random.seed(1000)

def subsample(dataset_name, split='dev', sample_size=100):
    with jsonlines.open(f"./datasets/{dataset_name}/{split}.jsonl") as reader:
        data = list(reader)
    
    data_sample = random.sample(data, sample_size)

    for item in tqdm(data_sample, total=sample_size):
        item["supporting_id"] = []
        for para in item['context']:
            if para['is_supporting']:
                query_result = query(dataset_name, para['content'])
                error_count = 2
                find_sp = False
                for i in range(error_count):
                    top_para = query_result.json()['retrieval'][i]
                    top_para_content = top_para['paragraph_text']
                    content = para['content']
                    if content == top_para_content or can_transform_by_spaces(content, top_para_content):
                        para['content'] = top_para_content
                        item['supporting_id'].append(top_para['id'])
                        find_sp = True
                        break
                if not find_sp:
                    ValueError("cann't find similar paragraph")
    
    with jsonlines.open(f"./datasets/{dataset_name}/{split}_sample_{sample_size}.jsonl", mode='w') as writer:
        writer.write_all(data_sample)


def main():
    parser = argparse.ArgumentParser(description='Subsample a dataset and process the paragraphs.')
    
    parser.add_argument('dataset_name', 
                        type=str, 
                        help='Name of the dataset to process (required)')
    
    parser.add_argument('--split', 
                        type=str, 
                        default='dev',
                        choices=['train', 'dev', 'test'],
                        help='Dataset split to process (default: dev)')
    
    parser.add_argument('--sample_size', 
                        type=int, 
                        default=100,
                        help='Number of samples to extract (default: 100)')
    
    args = parser.parse_args()

    subsample(args.dataset_name, args.split, args.sample_size)

if __name__ == "__main__":
    main()
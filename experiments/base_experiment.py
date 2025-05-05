from controller.multi_state_manager import MultiStateManager
import jsonlines
import os
import json
import argparse
from .utils import send_email
from metrics.evaluate import evaluate

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run experiments with configurable parameters.')
    parser.add_argument('--dataset_name', type=str, default="hotpotqa",
                       help='Name of the dataset to use (default: "hotpotqa")')
    parser.add_argument('--test_filename', type=str, default="dev_sample_100.jsonl",
                       help='Filename of the test data (default: "dev_sample_100.jsonl")')
    parser.add_argument('--test_size', type=int, default=100,
                       help='Number of test samples to use (default: 100)')
    
    parser.add_argument('--retrieval_method', type=str, default='elasticsearch',
                       help='Number of test samples to use (default: 100)')
    
    parser.add_argument('--skip_ground', type=bool, default=False,
                       help='Number of test samples to use (default: 100)')
    
    parser.add_argument('--retrieval_num', type=int, default=9,
                       help='Number of test samples to use (default: 100)')
    
    args = parser.parse_args()
    
    dataset_name = args.dataset_name
    test_filename = args.test_filename
    test_size = args.test_size

    with jsonlines.open(f"./datasets/{dataset_name}/{test_filename}") as reader:
        dataset = list(reader)[:test_size]

    ms_manager = MultiStateManager(dataset, dataset_name, retrieval_num=args.retrieval_num, skip_ground=args.skip_ground)

    # ms_manager.serial_test()

    ms_manager.parallel_test()
    
    experiment_name = "_".join(["base_experiment", 
                                dataset_name, 
                                test_filename.split('.')[0], 
                                str(test_size),
                                args.retrieval_method,
                                str(args.skip_ground),
                                str(args.retrieval_num)])

    os.makedirs(f"./log/{experiment_name}", exist_ok=True)
    with open(f"./log/{experiment_name}/results.json", 'w') as f:
        json.dump(ms_manager.test_results, f, ensure_ascii=False)
    eval_result = evaluate(ms_manager.test_results)
    print(eval_result)
    send_email(f"your experiments finished:")

if __name__ == "__main__":
    main()

from controller.multi_state_manager import MultiStateManager
import jsonlines
import os
import json
import argparse
from .utils import send_email

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run experiments with configurable parameters.')
    parser.add_argument('--datasets_name', type=str, default="hotpotqa",
                       help='Name of the dataset to use (default: "hotpotqa")')
    parser.add_argument('--test_filename', type=str, default="dev_sample_100.jsonl",
                       help='Filename of the test data (default: "dev_sample_100.jsonl")')
    parser.add_argument('--test_size', type=int, default=100,
                       help='Number of test samples to use (default: 100)')
    
    args = parser.parse_args()
    
    datasets_name = args.datasets_name
    test_filename = args.test_filename
    test_size = args.test_size

    with jsonlines.open(f"./datasets/{datasets_name}/{test_filename}") as reader:
        datasets = list(reader)[:test_size]

    ms_manager = MultiStateManager(datasets, datasets_name)

    ms_manager.serial_test()
    
    experiment_name = "_".join(["base_experiment", datasets_name, test_filename.split('.')[0], str(test_size)])

    os.makedirs(f"./log/{experiment_name}", exist_ok=True)
    with open(f"./log/{experiment_name}/results.json", 'w') as f:
        json.dump(ms_manager.test_results, f, ensure_ascii=False)

    send_email("your experiments finished")

if __name__ == "__main__":
    main()

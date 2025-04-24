from controller.multi_state_manager import MultiStateManager
import jsonlines
import os
import json
from .utils import send_email

def main():
    datasets_name = "musique"
    test_filename = "dev_sample_100.jsonl"
    test_size = 2
    with jsonlines.open(f"./datasets/{datasets_name}/{test_filename}") as reader:
        datasets = list(reader)[:test_size]

    ms_manager = MultiStateManager(datasets, datasets_name)

    ms_manager.serial_test()

    for idx, row in enumerate(datasets):
        row['test_result'] = ms_manager.test_results[idx]
        recall_fact_id = []
        max_iteration = len(row['test_result']) - 1
        for _, iteration in row['test_result'].items():
            iteration_recall_fact_id = []
            for doc in iteration['retrieved_docs']:
                iteration_recall_fact_id.append(doc['id'])
            recall_fact_id.append(iteration_recall_fact_id)
        row['recall_fact_id'] = recall_fact_id
        row['prediction'] = row['test_result'][max_iteration]['hypothesis']
    
    experiment_name = "_".join(["base_experiment", datasets_name, test_filename.split('.')[0], str(test_size)])

    os.makedirs(f"./log/{experiment_name}", exist_ok=True)
    with open(f"./log/{experiment_name}/results.json", 'w') as f:
        json.dump(datasets, f, ensure_ascii=False)

    send_email("your experiments finished")

if __name__ == "__main__":
    main()
from .state_manager import StateManager
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class MultiStateManager:
    def __init__(self, datasets, corpus_name, 
                 max_iterations=6, retrieval_num=9,
                 skip_ground=False, beta=2):
        self.datasets = datasets
        self.corpus_name = corpus_name
        self.test_results = []
        self.max_iterations = max_iterations
        self.retrieval_num = retrieval_num
        self.skip_ground = skip_ground
        self.beta = beta

    def serial_test(self):
        for row in tqdm(self.datasets, total=len(self.datasets)):
            state_manager = StateManager(row['question'], self.corpus_name,
                                         self.max_iterations, self.retrieval_num,
                                         self.skip_ground, self.beta)
            state_manager.run_full_cycle()
            self.test_results.append({
                "question": state_manager.question,
                "pred_answer": state_manager.answer,
                "gold_answer": row['answer'],
                "iteration_info": state_manager.iteration_info,
                "pred_sp_id": state_manager.supporting_fact_ids,
                "gold_sp_id": row['supporting_id'],
            })
            
    def parallel_test(self):
        max_workers = max(1, (os.cpu_count() or 1) - 12)
        max_workers = min(max_workers, 4)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._process_row, row): row 
                for row in self.datasets
            }
            
            with tqdm(total=len(self.datasets)) as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    self.test_results.append(result)
                    pbar.update(1)
                    
    def _process_row(self, row):
        state_manager = StateManager(row['question'], self.corpus_name,
                                         self.max_iterations, self.retrieval_num,
                                         self.skip_ground, self.beta)
        state_manager.run_full_cycle()
        return {
            "question": state_manager.question,
            "pred_answer": state_manager.answer,
            "gold_answer": row['answer'],
            "iteration_info": state_manager.iteration_info,
            "pred_sp_id": state_manager.supporting_fact_ids,
            "gold_sp_id": row['supporting_id'],
        }
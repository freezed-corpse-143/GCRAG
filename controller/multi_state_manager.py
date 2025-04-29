from .state_manager import StateManager
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class MultiStateManager:
    def __init__(self, datasets, corpus_name):
        self.datasets = datasets
        self.corpus_name = corpus_name
        self.test_results = []

    def serial_test(self):
        for row in tqdm(self.datasets, total=len(self.datasets)):
            state_manager = StateManager(row['question'], self.corpus_name)
            state_manager.run_full_cycle()
            self.test_results.append(state_manager.iteration_info)
            
    def parallel_test(self):
        max_workers = max(1, (os.cpu_count() or 1) - 8)
        max_workers = min(max_workers, 8)
        
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
        state_manager = StateManager(row['question'], self.corpus_name)
        state_manager.run_full_cycle()
        return state_manager.iteration_info
from .state_manager import StateManager
from tqdm import tqdm

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
            

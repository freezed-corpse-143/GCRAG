from typing import List, Optional, Dict
from .states import *
from .utils import retrieve, generate
from prompts.decompose import decompose_prompt
from prompts.ground import revise_prompt

class StateManager:
    def __init__(self, original_question: str, corpus_name: str, max_iterations: int = 5):
        self.original_question = original_question
        self.corpus_name = corpus_name
        self.max_iterations = max_iterations
        self.current_state: State = InitialState(original_question)
        self.iteration_info= dict()
        
        # 初始化第0轮信息（初始假设为空字符串）
        self.iteration_info[0] = {
            'hypothesis': "",
            'subquestion': None,
            'retrieved_docs': None
        }
    
    def initialize(self) -> State:
        """初始化状态"""
        self.current_state = InitialState(
            original_question=self.original_question,
            current_hypothesis="",
            iteration=0  # 第0轮
        )
        return self.current_state
    
    def generate_subquestion(self) -> SubquestionState:
        current_iter = self.current_state.iteration

        prompt = decompose_prompt.format(
            original_question = self.original_question,
            current_hypothesis = self.current_state.current_hypothesis,
        ).strip()
        
        generated_result = generate(prompt)
        subquestion = generated_result['generated_text'].strip()
        
        self.iteration_info[current_iter]['subquestion'] = subquestion
        
        self.current_state = SubquestionState(
            original_question=self.original_question,
            current_hypothesis=self.current_state.current_hypothesis,
            subquestion=subquestion,
            previous_hypothesis=self.current_state.current_hypothesis,
            iteration=current_iter
        )
        return self.current_state
    
    def retrieve_documents(self) -> RetrievalState:
        
        current_iter = self.current_state.iteration
        retrieved_results = retrieve(self.corpus_name, self.current_state.subquestion)
        retrieved_docs = retrieved_results['retrieval']
        
        self.iteration_info[current_iter]['retrieved_docs'] = retrieved_docs
        
        self.current_state = RetrievalState(
            original_question=self.original_question,
            current_hypothesis=self.current_state.current_hypothesis,
            subquestion=self.current_state.subquestion,
            retrieved_documents=retrieved_docs,
            previous_hypothesis=self.current_state.previous_hypothesis,
            iteration=current_iter
        )
        return self.current_state
    
    def refine_hypothesis(self) -> State:
        current_iter = self.current_state.iteration
        
        if self._should_terminate():
            return self._finalize()
        
        prompt = revise_prompt.format(
            original_question = self.original_question,
            current_hypothesis = self.current_state.current_hypothesis,
            subquestion = self.current_state.subquestion,
            retrieved_documents = self.current_state.retrieved_documents
        ).strip()
        
        generated_result = generate(prompt)
        new_hypothesis = generated_result['generated_text'].strip()
        new_iter = current_iter + 1
        
        self.iteration_info[new_iter] = {
            'hypothesis': new_hypothesis,
            'subquestion': None,
            'retrieved_docs': None
        }
        
        self.current_state = SubquestionState(
            original_question=self.original_question,
            current_hypothesis=new_hypothesis,
            previous_hypothesis=self.current_state.current_hypothesis,
            iteration=new_iter
        )
        return self.current_state
    
    def _should_terminate(self) -> bool:
        current_iter = self.current_state.iteration
        
        if current_iter >= self.max_iterations:
            return True
        
        if current_iter >= 1:
            prev_hypothesis = self.iteration_info[current_iter-1]['hypothesis']
            current_hypothesis = self.current_state.current_hypothesis
            if prev_hypothesis == current_hypothesis:
                return True
        
        return False
    
    def _finalize(self) -> FinalState:
        all_subquestions = [
            info['subquestion'] 
            for iter_num, info in sorted(self.iteration_info.items())
            if info['subquestion'] is not None
        ]
        
        all_retrieved_docs = [
            info['retrieved_docs'] 
            for iter_num, info in sorted(self.iteration_info.items())
            if info['retrieved_docs'] is not None
        ]
        
        all_hypotheses = [
            info['hypothesis'] 
            for iter_num, info in sorted(self.iteration_info.items())
        ]
        
        self.current_state = FinalState(
            original_question=self.original_question,
            current_hypothesis=all_hypotheses[-1],
            subquestions=all_subquestions,
            retrieved_documents=all_retrieved_docs,
            all_hypotheses=all_hypotheses,
            iteration=self.current_state.iteration
        )
        return self.current_state
    
    def run_full_cycle(self):
        # try:
        self.initialize()
        
        while not isinstance(self.current_state, FinalState):
            self.generate_subquestion()
            
            self.retrieve_documents()
            
            state = self.refine_hypothesis()
            
            if isinstance(state, FinalState):
                break
            
        return self.current_state
        
        # except Exception as e:
        #     print(f"Error during multi-hop QA: {str(e)}")
        #     return self._finalize()
    
    def get_iteration_info(self, iteration: int) -> Dict[str, any]:
        return self.iteration_info.get(iteration, {})

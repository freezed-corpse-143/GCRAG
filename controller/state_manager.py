from typing import Dict
from .states import State, RetrievalState
from .utils import retrieve, generate, extract_thought_answer, format_retr_docs, extract_answer, parse_json
from prompts.decompose_template import decompose_prompt, decompose_instructions
from prompts.ground_template import ground_prompt, ground_instrcutions
from prompts.examples import decompose_examples, ground_examples

class StateManager:
    def __init__(self, question: str, corpus_name: str, max_iterations: int = 5, retrieval_num: int = 3, skip_ground: bool = False):
        self.question = question
        self.corpus_name = corpus_name
        self.max_iterations = max_iterations
        self.retrieval_num = retrieval_num
        self.current_state = None
        self.iteration_info= dict()
        self.is_terminated = False
        self.decompose_examples_prompt = decompose_examples[corpus_name]
        self.ground_examples_prompt = ground_examples[corpus_name]
        self.supporting_fact_id = []
        self.answer = None
        self.skip_ground = skip_ground
        
    def initialize(self) -> State:
        self.current_state = State(
            thought="",
            answer= "",
            iteration=0
        )
        return self.current_state
    
    def generate_thought_answer(self) -> State:
        current_iter = self.current_state.iteration
        if current_iter not in self.iteration_info:

            prompt = decompose_prompt.format(
                instructions = decompose_instructions,
                examples = self.decompose_examples_prompt,
                question = self.question,
                thoughts_and_answers = self.get_thoughts_and_answers(),
            ).strip()
            
            thought_answer_list = []
            while not thought_answer_list:
                generated_result = generate(prompt)
                generated_text = generated_result['generated_text'].strip()
                # print(f"{current_iter+1} thought_answer: {generated_text}")
                thought_answer_list = extract_thought_answer(generated_text)
                # prompt += " "
            for idx, (thought, answer) in enumerate(thought_answer_list):
                self.iteration_info[current_iter+idx] = {
                    'thought': thought,
                    'answer': answer,
                    'retrieved_docs': [],
                }
        
        self.current_state = State(
            thought=self.iteration_info[current_iter]['thought'],
            answer=self.iteration_info[current_iter]['answer'],
            iteration=current_iter
        )

        if self._should_terminate():
            self.is_terminated = True
            return
        
        return self.current_state
    
    def retrieve_documents(self) -> RetrievalState:
        
        current_iter = self.current_state.iteration
        retrieved_results = retrieve(self.corpus_name, self.current_state.thought)
        retrieved_docs = retrieved_results['retrieval'][:self.retrieval_num]
        
        self.iteration_info[current_iter]['retrieved_docs'] = retrieved_docs
        
        self.current_state = RetrievalState(
            thought=self.current_state.thought,
            answer=self.current_state.answer,
            retrieved_docs=retrieved_docs,
            iteration=current_iter
        )
        return self.current_state
    
    def ground_truth(self) -> State:
        current_iter = self.current_state.iteration

        prompt = ground_prompt.format(
            instructions = ground_instrcutions,
            examples = self.ground_examples_prompt,
            retrieved_documents = format_retr_docs(self.current_state.retrieved_docs),
            question = self.question,
            answer = self.current_state.answer,
        ).strip()
        
        answer_ok = False
        while not answer_ok:
            generated_result = generate(prompt)
            generated_text = generated_result['generated_text'].strip()
            result = parse_json(generated_text)
            if "answer" not in result or "citation" not in result:
                continue
            self.iteration_info[current_iter]['answer'] = result['answer']
            # print(result)
            for item in result['citation']:
                if item in "123":
                    self.supporting_fact_id.append(
                        self.iteration_info[current_iter]['retrieved_docs'][int(item)-1]['id']
                    )
            answer_ok = True

        new_iter = current_iter + 1
        self.current_state = State(
            thought=self.current_state.thought,
            answer=result['answer'],
            iteration=new_iter
        )

        return self.current_state
    
    def _should_terminate(self) -> bool:
        if self.current_state.iteration >= self.max_iterations:
            self.answer = "Unknown"
            return True
        
        if "FINISH" in self.current_state.answer:
            self.answer = extract_answer(self.current_state.answer)
            return True
        
        return False
    
    def run_full_cycle(self):
        # try:
        self.initialize()
        
        while not self.is_terminated:
            self.generate_thought_answer()
            
            self.retrieve_documents()
            if not self.skip_ground:
                self.ground_truth()
        
        if self.skip_ground:
            for item in self.iteration_info.values():
                for d in item['retrieved_docs']:
                    self.supporting_fact_id.append(d['id'])
        self.supporting_fact_id = list(set(self.supporting_fact_id))
        return self.current_state
        
        # except Exception as e:
        #     print(f"Error during multi-hop QA: {str(e)}")
        #     return self._finalize()
    
    def get_iteration_info(self, iteration: int) -> Dict[str, any]:
        return self.iteration_info.get(iteration, {})
    
    def get_thoughts_and_answers(self):
        result = ""
        for key, value in self.iteration_info.items():
            result += f"Thought {key+1}: {value['thought']}\nAnswer {key+1}: {value['answer']}\n"
        return result.strip()

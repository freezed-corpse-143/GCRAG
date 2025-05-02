from typing import Dict
from .utils import retrieve, generate, extract_thought_answer, format_retr_docs, extract_answer, parse_json
from prompts.decompose_template import decompose_prompt, decompose_instructions
from prompts.ground_template import ground_prompt, ground_instrcutions
from prompts.examples import decompose_examples, ground_examples

class StateManager:
    def __init__(self, question: str, corpus_name: str, max_iterations: int = 5, 
                 retrieval_num: int = 3, skip_ground: bool = False, 
                 beta: int = 1):
        self.question = question
        self.corpus_name = corpus_name
        self.max_iterations = max_iterations
        self.retrieval_num = retrieval_num
        self.skip_ground = skip_ground
        self.beta = beta

        self.iteration_info= dict()
        self.decompose_examples_prompt = decompose_examples[corpus_name]
        self.ground_examples_prompt = ground_examples[corpus_name]
        self.supporting_fact_id = []
        
        # state
        self.current_iter = 0
        self.thought = None
        self.answer = None
        self.is_terminated = False
        self.retrieved_docs = None
        
    
    def generate_thought_answer(self):
        current_iter = self.current_iter
        if current_iter not in self.iteration_info:
            prompt = decompose_prompt.format(
                instructions = decompose_instructions,
                examples = self.decompose_examples_prompt,
                question = self.question,
                thoughts_and_answers = self.get_thoughts_and_answers(),
            ).strip()
            
            thought_answer_list = []
            # print("start to generate")
            while not thought_answer_list:
                generated_result = generate(prompt)
                generated_text = generated_result['generated_text'].strip()
                # print(generated_result['run_time_in_seconds'])
                # print(f"{current_iter+1} thought_answer: {generated_text}")
                thought_answer_list = extract_thought_answer(generated_text)
                prompt += " "
            # print("generate time:" ,generated_result['run_time_in_seconds'])
            for idx, (thought, answer) in enumerate(thought_answer_list):
                self.iteration_info[current_iter+idx] = {
                    'thought': thought,
                    'answer': answer,
                    'retrieved_docs': [],
                }
        
        self.thought=self.iteration_info[current_iter]['thought']
        self.answer=self.iteration_info[current_iter]['answer']

        if self._should_terminate():
            self.is_terminated = True
    
    def retrieve_documents(self):
        current_iter = self.current_iter
        # print(self.thought)
        # print(self.iteration_info)
        # print("start to retrieve")
        retrieved_results = retrieve(self.corpus_name, self.question + (" " +self.thought) * self.beta)
        # retrieved_results = retrieve(self.corpus_name, (" " +self.thought) * self.beta)
        # print("retrieved time:", retrieved_results['time_in_seconds'])
        self.retrieved_docs = retrieved_results['retrieval'][:self.retrieval_num]
        self.iteration_info[current_iter]['retrieved_docs'] = self.retrieved_docs
        
    
    def ground_truth(self):
        current_iter = self.current_iter

        prompt = ground_prompt.format(
            instructions = ground_instrcutions,
            examples = self.ground_examples_prompt,
            retrieved_documents = format_retr_docs(self.retrieved_docs),
            question = self.question,
            answer = self.answer,
        ).strip()
        
        answer_ok = False
        while not answer_ok:
            generated_result = generate(prompt)
            generated_text = generated_result['generated_text'].strip()
            result = parse_json(generated_text)
            if "answer" not in result or "citation" not in result:
                prompt += " "
                continue
            self.iteration_info[current_iter]['answer'] = result['answer']
            # print(result)
            for item in result['citation']:
                if item in "123":
                    self.supporting_fact_id.append(
                        self.iteration_info[current_iter]['retrieved_docs'][int(item)-1]['id']
                    )
            answer_ok = True
    
    def _should_terminate(self) -> bool:
        if self.current_iter >= self.max_iterations:
            self.answer = "Unknown"
            return True
        
        if "FINISH" in self.answer:
            self.answer = extract_answer(self.answer)
            return True
        
        return False
    
    def run_full_cycle(self):
        
        while not self.is_terminated:
            self.generate_thought_answer()
            
            self.retrieve_documents()
            if not self.skip_ground:
                self.ground_truth()
            self.current_iter += 1
        
        if self.skip_ground:
            for item in self.iteration_info.values():
                for d in item['retrieved_docs']:
                    self.supporting_fact_id.append(d['id'])
        self.supporting_fact_id = list(set(self.supporting_fact_id))
        
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

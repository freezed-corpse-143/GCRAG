from typing import Dict
from utils.serve import (
    generate,
    retrieve
)

from utils.string import (
    extract_thought_answer, 
    extract_answer, 
    format_sp
)

import time

from prompts.GenGround import (
    decompose_prompt, 
    answer_format_prompt,
    decompose_examples_prompt,
    ground_examples
)

from rerank.llm_filter import batch_ground_step

class GenGround:
    def __init__(self, question: str, corpus_name: str, max_iterations: int = 6, 
                 retrieval_num: int = 3, skip_ground: bool = False, 
                 beta: int = 2):
        self.question = question
        self.corpus_name = corpus_name
        self.max_iterations = max_iterations
        self.retrieval_num = retrieval_num
        self.skip_ground = skip_ground
        self.beta = beta

        self.iteration_info= dict()
        self.decompose_examples_prompt = decompose_examples_prompt
        self.ground_examples_prompt = ground_examples[corpus_name]
        self.supporting_fact_ids = []
        self.supporting_fact_docs = []
        self.supporting_fact_ids = []
        self.supporting_fact_docs = []
        self.elapsed_time = 0.
        
        # state
        self.current_iter = 0
        self.thought = question
        self.answer = "No sufficient information."
        self.is_terminated = False
        self.retrieved_docs = None
        self.iteration_info[self.current_iter] = {
            'thought': self.thought,
            'answer': self.answer,
            'retrieved_docs': [],
            'supporting_fact': [],
        }
        
    def reason(self):
        # print("reason")
        current_iter = self.current_iter
        prompt = decompose_prompt.format(
            examples = self.decompose_examples_prompt,
            question = self.question,
            thoughts_and_answers = self.get_thoughts_and_answers(),
            # supporting_facts = format_sp(self.supporting_fact_docs),
        ).strip()
        
        try:
            while True:
                response = generate(prompt, stop=['\nThought', '\nthought'])['generated_text'].strip()
                thought, answer = extract_thought_answer(response)
                if not thought:
                    prompt += ". Please generate \"Thought: \" as the prefix"
                    continue
                if answer:
                    break
                response = generate(prompt+f"\nThought: {thought}", stop=['\nThought', '\nthought'])['generated_text'].strip()
                _, answer = extract_thought_answer(response)
                if not answer:
                    answer = response.replace("Answer", "").replace(":", "").strip()
                break
        except Exception as e:
            print(e)
            thought = f"rethink original quesiton: {self.question}"
            answer = "thus, therefore, so"


        self.iteration_info[current_iter] = {
            'thought': thought,
            'answer': answer,
            'retrieved_docs': [],
            'supporting_fact': [],
        }
        
        self.thought=thought
        self.answer=answer

        self.is_terminated = self._should_terminate()
    
    def retrieve(self):
        # print('retrieve')
        current_iter = self.current_iter
        retrieved_results = retrieve(self.question+(" " +self.thought) * self.beta)
        self.retrieved_docs = retrieved_results['retrieval']
        self.iteration_info[current_iter]['retrieved_docs'] = self.retrieved_docs
        
    def ground_truth(self):
        # print("ground")
        current_iter = self.current_iter

        answer, sp_docs, = batch_ground_step(
            examples=self.ground_examples_prompt,
            question=self.question,
            retrieved_documents = self.retrieved_docs[:self.retrieval_num],
            thought=self.thought,
            answer=self.answer,
        )
        self.iteration_info[current_iter]['supporting_fact'] = sp_docs
        self.iteration_info[current_iter]['answer'] = answer
        self.answer = answer
        for doc in sp_docs:
            if doc['id'] not in self.supporting_fact_ids:
                self.supporting_fact_docs.append(doc)
                self.supporting_fact_ids.append(doc['id'])
        
    def _should_terminate(self) -> bool:
        result = False
        if self.current_iter >= self.max_iterations:
            result = True
        
        if "FINISH" in self.answer:
            result = True

        return result
    
    def run_full_cycle(self):
        # print("start cycle")
        start_time = time.time()
        while not self.is_terminated:
            self.retrieve()
            if not self.skip_ground:
                self.ground_truth()
            self.current_iter += 1
            self.reason()
        self.format_final_answer()
        # print(self.answer)
        if self.skip_ground:
            for item in self.iteration_info.values():
                for d in item['retrieved_docs']:
                    self.supporting_fact_ids.append(d['id'])
                    self.supporting_fact_ids.append(d['id'])

        end_time = time.time()
        self.elapsed_time = end_time - start_time
    
    def get_iteration_info(self, iteration: int) -> Dict[str, any]:
        return self.iteration_info.get(iteration, {})
    
    def get_thoughts_and_answers(self):
        result = ""
        for key, value in self.iteration_info.items():
            result += f"Thought {key+1}: {value['thought']}\nAnswer {key+1}: {value['answer']}\n"
        return result.strip()
    
    def format_final_answer(self):
        if self.skip_ground:
            pass
        elif "FINISH" in self.answer:
            self.answer = extract_answer(self.answer)
            self.iteration_info[self.current_iter-1]['answer'] = self.answer
        else:
            # answer, sp_docs, = batch_ground_step(
            #     examples=self.ground_examples_prompt,
            #     question=self.question,
            #     retrieved_documents = self.supporting_fact_docs,
            #     thought=self.get_thoughts_and_answers(),
            #     answer=self.answer,
            # )

            prompt = answer_format_prompt.format(
                question=self.question,
                answer=self.answer
            )
            format_answer = None
            while not format_answer:
                generated_result = generate(prompt)
                generated_text = generated_result['generated_text'].strip()
                format_answer = extract_answer(generated_text)
                if format_answer:
                    break
                prompt += ". Please put final answer in \"FINISH[]\"."
            self.answer = format_answer
            self.iteration_info[self.current_iter-1]['answer'] = format_answer
        # print(self.current_iter)
        # print(self.answer)

        

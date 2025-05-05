from typing import Dict
from .utils import retrieve, generate, extract_thought_answer, extract_answer, format_sp
from prompts.template import decompose_prompt, answer_format_prompt
from prompts.examples import decompose_examples, ground_examples
from rerank.ner_filter import ner_filter
from rerank.llm_filter import ground_step


class StateManager:
    def __init__(self, question: str, corpus_name: str, max_iterations: int = 6, 
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
        self.supporting_fact_ids = []
        self.supporting_fact_docs = []
        
        # state
        self.current_iter = 0
        self.thought = None
        self.answer = None
        self.is_terminated = False
        self.retrieved_docs = None
        
    def generate_thought_answer(self):
        current_iter = self.current_iter
        prompt = decompose_prompt.format(
            examples = self.decompose_examples_prompt,
            question = self.question,
            thoughts_and_answers = self.get_thoughts_and_answers(),
            supporting_facts = format_sp(self.supporting_fact_docs),
        ).strip()
        
        thought_answer_list = []
        # print("start to generate")
        try:
            while not thought_answer_list:
                generated_result = generate(prompt)
                generated_text = generated_result['generated_text'].strip()
                # print(generated_result['run_time_in_seconds'])
                # print(f"{current_iter+1} thought_answer: {generated_text}")
                thought_answer_list = extract_thought_answer(generated_text)
                prompt += "."
        except Exception as e:
            print(e)
            # print(prompt)
            # raise ValueError("generate error")
            thought_answer_list = [f"rethink original quesiton: {self.question}", "thus, therefore, so"]
        # print("generate time:" ,generated_result['run_time_in_seconds'])
        self.iteration_info[current_iter] = {
            'thought': thought_answer_list[0],
            'answer': thought_answer_list[1],
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
        retrieved_results = retrieve(self.question + (" " +self.thought) * self.beta)
        # retrieved_results = retrieve(self.corpus_name, (" " +self.thought) * self.beta)
        # print("retrieved time:", retrieved_results['time_in_seconds'])
        self.retrieved_docs = retrieved_results['retrieval']
        self.iteration_info[current_iter]['retrieved_docs'] = self.retrieved_docs
        
    def ground_truth(self):
        current_iter = self.current_iter

        sp_docs, sp_ids = ner_filter(
            question=self.question,
            retrieved_documents=self.retrieved_docs[:self.retrieval_num],
            thought=self.thought,
        )

        answer, sp_docs, sp_ids = ground_step(
            examples=self.ground_examples_prompt,
            question=self.question,
            retrieved_documents = sp_docs,
            thought=self.thought,
            answer=self.answer,
        )

        self.iteration_info[current_iter]['answer'] = answer
        for id, doc in zip(sp_ids, sp_docs):
            if id not in self.supporting_fact_ids:
                self.supporting_fact_docs.append(doc)
                self.supporting_fact_ids.append(id)
        
    def _should_terminate(self) -> bool:
        if self.current_iter >= self.max_iterations:
            new_answer, new_supporting_docs, new_supporting_ids = ground_step(
                examples=self.ground_examples_prompt,
                question=self.question,
                retrieved_documents = self.supporting_fact_docs,
                thought=self.get_thoughts_and_answers(),
                answer=self.answer,
            )
            self.supporting_fact_docs = new_supporting_docs
            self.supporting_fact_ids = new_supporting_ids

            prompt = answer_format_prompt.format(
                question=self.question,
                answer=new_answer
            )
            format_answer = None
            while not format_answer:
                generated_result = generate(prompt)
                generated_text = generated_result['generated_text'].strip()
                format_answer = extract_answer(generated_text)
                if format_answer:
                    break
                prompt += "."
            self.answer = format_answer
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
                    self.supporting_fact_ids.append(d['id'])
        self.supporting_fact_ids = list(set(self.supporting_fact_ids))
        
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

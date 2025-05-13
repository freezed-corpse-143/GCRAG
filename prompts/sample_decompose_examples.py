import random
import jsonlines
from utils.serve import generate
import argparse
from tqdm import tqdm
import re

random.seed(42)

format_examples_prompt = '''
Let's think step by step.
- Thought: reason about the current situation and formulate a sub-question. Your Thought process should aim to formulate as simple and specific a question as possible, which should include a clear description of the key entities’ features.
- Answer:  answer the sub-question proposed in the Thought step and give some explanations.

Format:
Question: a complex question
Thought 1: The first sub-question
Answer 1: Answer the first sub-question
... (the Thought and Answer steps can repeat N times)
Thought n: The n-th sub-question
Answer n:  Answer the n-th sub-question
Thought n+1: the final thought
Answer n+1: FINISH[the final answer]

Please read the input question, answer and supporting facts, follow these instructions:
1. Your output should be in the format above.
2. Question be filled with input quesiton.
3. Each supporting fact should be used to generate "Thought" and "Answer".
4. Last thought should foucs on the original question. Last Answer should be in the format of "Answer n: FINISH[<input answer>]", which is filled with the input answer.
'''

def _format_row(row):
    result = f'''
    <question>{row['question']}</question>\n<answer>{row['answer'][0]}</answer>
    '''.strip()
    for ct in row['context']:
        if ct['is_supporting']:
            result += f"\n<supporing fact>{ct['content']}</supporing fact>"
    return result

def check_answer_pattern(text):
    pattern = r'Answer \d+: FINISH\[.*\]'
    matches = re.findall(pattern, text)
    if matches:
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser(description='Sample a dataset and generate examples.')
    
    parser.add_argument('dataset', 
                        default="hotpotqa",
                        type=str, 
                        help='Name of the dataset to process (required)')
    
    args = parser.parse_args()

    with jsonlines.open(f"./datasets/{args.dataset}/train.jsonl") as reader:
        data = list(reader)

    sample_data = random.sample(data, 100)

    pattern = r'Answer \d+: FINISH\[.*\]'

    result = []

    for row in tqdm(sample_data, total=100):
        generate_ok = False
        generated_text = None
        suffix = ""
        while not generate_ok:
            prompt = format_examples_prompt + _format_row(row)  + suffix
            generated_result = generate(prompt)
            generated_text = generated_result['generated_text'].replace("\n\n", "\n")
            matches = re.findall(pattern, generated_text)
            # if matches:
            generate_ok = True
            # suffix += f"\nPlease make last answer match 'Answer <number>: FINISH[<input answer>]'"

        result.append(generated_text)
    
    valid_data = []
    for idx, item in enumerate(result):
        if not check_answer_pattern(item):
            continue
        lines = item.strip().split("\n")
        question = sample_data[idx]['question']
        lines[0] = f"Question: {question}"
        final_answer = sample_data[idx]['answer']
        lines[-1] = lines[-1][:len("Answer 3: ")] + f"FINISH[{final_answer}]"
        valid_data.append("\n".join(lines))

    with open(f"./prompts/decompose_{args.dataset}.txt", 'w') as f:
        f.write("\n\n".join(valid_data))
    

if __name__ == "__main__":
    main()
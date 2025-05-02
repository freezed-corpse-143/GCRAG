import random
import jsonlines
from .utils import generate
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
Answer 1: answer the first sub-question
... (the Thought and Answer steps can repeat N times)
Thought n: the final thought
Answer n: FINISH[the final answer]

Please read the input question, answer and supporting facts, follow these instructions:
1. Your output should be in the format above.
2. Question be filled with input quesiton.
3. Each supporting fact should be used to generate "Thought" and "Answer".
4. Last thought should foucs on the question. Last Answer should be in the format of "Answer n: FINISH[<input answer>]", which is filled with the input answer.
'''

def _format_row(row):
    result = f'''
    <question>{row['question']}</question>\n<answer>{row['answer'][0]}</answer>
    '''.strip()
    for ct in row['context']:
        if ct['is_supporting']:
            result += f"\n<supporing fact>{ct['content']}</supporing fact>"
    return result

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
    
    with open(f"./prompts/{args.dataset}.txt", 'w') as f:
        f.write("\n\n".join(result))
    


if __name__ == "__main__":
    main()
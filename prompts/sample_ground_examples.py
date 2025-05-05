from rapidfuzz import fuzz
from tqdm import tqdm
import jsonlines
from .utils import generate
import argparse

wrong_answer_prompt = '''
Please read input question, thoughts, answers, and generate one wrong answer for each answer.
Generate "Wrong answer x: ..." for "Answer x: ...".

Input:
{content}
output:
'''.strip()

def similarity(s1, s2):
    return fuzz.WRatio(s1, s2) / 100

def main():
    parser = argparse.ArgumentParser(description='Sample a dataset and generate examples.')
    
    parser.add_argument('dataset', 
                        default="hotpotqa",
                        type=str, 
                        help='Name of the dataset to process (required)')
    
    args = parser.parse_args()
    dataset = args.dataset

    with jsonlines.open(f"./datasets/{dataset}/train.jsonl") as reader:
        train_data = list(reader)
    
    q_sp = dict()
    for row in train_data:
        sp_content = []
        for para in row['context']:
            if para['is_supporting']:
                sp_content.append(para['content'])
        sp_content = list(set(sp_content))
        q_sp[row['question'].strip()] = sp_content

    with open(f"./prompts/decompose_{dataset}.txt") as f:
        decompose_examples = f.read().split("\n\n")

    decompose_sp = []
    for e in decompose_examples:
        question = e.strip().split('\n')[0][len("question:"):].strip()
        if question in q_sp:
            decompose_sp.append(q_sp[question])
            continue
        find_q = False
        best_score = .0
        for q in q_sp:
            score = similarity(question, q)
            if score > best_score:
                best_score = score
            if score > 0.97:
                decompose_sp.append(q_sp[q])
                find_q = True
                break
        if not find_q:
            print(best_score)
            raise ValueError(f"No sufficiently matching question")
    
    wrong_answer_results = []
    for de in tqdm(decompose_examples, total=len(decompose_examples)):
        prompt = wrong_answer_prompt.format(
            content = de.strip()
        )
        
        result = generate(prompt)
        wrong_answer_results.append(result['generated_text'].replace("\n\n", "\n"))

    results = []
    for id in range(len(decompose_examples)):
        de = decompose_examples[id].strip() + "\n"
        sp_list = decompose_sp[id]
        sp_content = ""
        for sp in sp_list:
            sp_content += f"Document : {sp}\n"
        wrong_answer = wrong_answer_results[id]
        
        results.append(
            de+sp_content+wrong_answer
        )
    
    with open(f"./prompts/ground_{dataset}.txt", 'w') as f:
        f.write("\n\n".join(results))

if __name__ == "__main__":
    main()

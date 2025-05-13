import re, string
from utils.serve import generate
from tqdm import tqdm
from collections import Counter

def normalize_answer(s):
    """Normalize answer for comparison."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def _prec_recall_f1_score(pred_items, gold_items):
    """
    Compute precision, recall and f1 given a set of gold and prediction items.

    :param pred_items: iterable of predicted values
    :param gold_items: iterable of gold values

    :return: tuple (p, r, f1) for precision, recall, f1
    """
    common = Counter(gold_items) & Counter(pred_items)
    num_same = sum(common.values())
    if num_same == 0:
        return 0, 0, 0
    precision = 1.0 * num_same / len(pred_items)
    recall = 1.0 * num_same / len(gold_items)
    f1 = (2 * precision * recall) / (precision + recall)
    return precision, recall, f1

def single_f1_score(guess, answers):
    if guess is None or answers is None:
        return 0
    g_tokens = normalize_answer(guess).split()
    scores = [
        _prec_recall_f1_score(g_tokens, normalize_answer(a).split()) for a in answers
    ]
    return [f1 for p, r, f1 in scores]


em_eva_prompt = '''
You will be provided with a question, a golden answer, and a predicted answer. 
Please judge whether the predicted answer is semantically equivalent to the golden answer. 
You only need to respond with True or False.

Question: {question}
golden answer: {gold_answer}
predicted answer: {pred_answer}
'''.strip()
    
def evaluate(info):
    result = {
        "answer_em": 0.,
        "answer_precision": 0.,
        "answer_recall": 0.,
        "answer_f1": 0.,
        "sp_em": 0.,
        "sp_precision": 0.,
        "sp_recall": 0.,
        "sp_f1": 0.,
        "joint_em": 0.,
        "joint_precision": 0.,
        "joint_recall": 0.,
        "joint_f1": 0.,
    }
    
    total_items = len(info)
    
    for item in tqdm(info, total=total_items):
        # Answer evaluation
        pred_answer = item['pred_answer']
        pred_answer_tokens = set(normalize_answer(item['pred_answer']).split())
        best_answer_f1 = 0.
        best_answer_em = 0.
        best_answer_precision = 0.
        best_answer_recall = 0.
        
        for gold_answer in item['gold_answer']:
            gold_answer_tokens = set(normalize_answer(gold_answer).split())
            answer_common_tokens = pred_answer_tokens & gold_answer_tokens
            
            # Handle division by zero cases
            precision = len(answer_common_tokens) / len(pred_answer_tokens) if len(pred_answer_tokens) > 0 else 0
            recall = len(answer_common_tokens) / len(gold_answer_tokens) if len(gold_answer_tokens) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            if f1 > best_answer_f1:
                best_answer_f1 = f1
                # best_answer_em = int(pred_answer == gold_answer)
                eval_result = generate(em_eva_prompt.format(
                    question=item['question'],
                    gold_answer=gold_answer,
                    pred_answer=pred_answer,
                ))['generated_text']
                best_answer_em = int("true" in eval_result.lower())
                best_answer_precision = precision
                best_answer_recall = recall
            
            
            

        # print(best_answer_em)
        # Supporting facts evaluation
        pred_sp = set(item['pred_sp_id'])
        gold_sp = set(item['gold_sp_id'])
        common_sp = pred_sp & gold_sp
        
        sp_precision = len(common_sp) / len(pred_sp) if len(pred_sp) > 0 else 0
        sp_recall = len(common_sp) / len(gold_sp) if len(gold_sp) > 0 else 0
        sp_f1 = 2 * sp_precision * sp_recall / (sp_precision + sp_recall) if (sp_precision + sp_recall) > 0 else 0
        sp_em = int(pred_sp == gold_sp)
        
        # Joint evaluation
        joint_em = best_answer_em * sp_em
        joint_precision = (best_answer_precision + sp_precision) / 2
        joint_recall = (best_answer_recall + sp_recall) / 2
        joint_f1 = (best_answer_f1 + sp_f1) / 2
        
        # Accumulate results
        result['answer_em'] += best_answer_em
        result['answer_precision'] += best_answer_precision
        result['answer_recall'] += best_answer_recall
        result['answer_f1'] += best_answer_f1
        
        result['sp_em'] += sp_em
        result['sp_precision'] += sp_precision
        result['sp_recall'] += sp_recall
        result['sp_f1'] += sp_f1
        
        result['joint_em'] += joint_em
        result['joint_precision'] += joint_precision
        result['joint_recall'] += joint_recall
        result['joint_f1'] += joint_f1
    
    # Average the results
    for key in result:
        result[key] /= total_items
    
    return result
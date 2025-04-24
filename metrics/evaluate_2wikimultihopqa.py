import re
import string
from collections import Counter

def evaluate_2wikimultihopqa(data):
    """
    Evaluate 2WikiMultihopQA predictions with the given data format.
    
    Args:
        data: List of dicts with keys:
            - answer: list of ground truth answers (with aliases)
            - supporting_id: list of ground truth supporting fact IDs
            - recall_fact_id: list of lists of retrieved fact IDs per retrieval step
            - prediction: model's predicted answer
    
    Returns:
        dict with evaluation metrics
    """
    metrics = {
        'em': 0, 'f1': 0, 'prec': 0, 'recall': 0,
        'sp_em': 0, 'sp_f1': 0, 'sp_prec': 0, 'sp_recall': 0,
        'retrieval_recall': 0, 'retrieval_precision': 0, 'retrieval_f1': 0,
        'count': len(data)
    }

    for item in data:
        # Answer evaluation
        max_em, max_f1, max_prec, max_recall = 0, 0, 0, 0
        for gold_answer in item['answer']:
            em = int(normalize_answer(item['prediction']) == normalize_answer(gold_answer))
            f1, prec, recall = f1_score(item['prediction'], gold_answer)
            
            max_em = max(max_em, em)
            max_f1 = max(max_f1, f1)
            max_prec = max(max_prec, prec)
            max_recall = max(max_recall, recall)
        
        metrics['em'] += max_em
        metrics['f1'] += max_f1
        metrics['prec'] += max_prec
        metrics['recall'] += max_recall

        # Supporting facts evaluation
        predicted_support = [[pid, 0] for pid in set().union(*item['recall_fact_id'])]  # Format as [pid, score]
        gold_support = [[pid, 0] for pid in item['supporting_id']]
        
        # Calculate supporting facts metrics
        cur_sp_pred = normalize_sp(set(map(tuple, predicted_support)))
        gold_sp_pred = normalize_sp(set(map(tuple, gold_support)))
        
        tp, fp, fn = 0, 0, 0
        for e in cur_sp_pred:
            if e in gold_sp_pred:
                tp += 1
            else:
                fp += 1
        for e in gold_sp_pred:
            if e not in cur_sp_pred:
                fn += 1
                
        sp_prec = 1.0 * tp / (tp + fp) if tp + fp > 0 else 0.0
        sp_recall = 1.0 * tp / (tp + fn) if tp + fn > 0 else 0.0
        sp_f1 = 2 * sp_prec * sp_recall / (sp_prec + sp_recall) if sp_prec + sp_recall > 0 else 0.0
        sp_em = 1.0 if fp + fn == 0 else 0.0
        
        metrics['sp_em'] += sp_em
        metrics['sp_f1'] += sp_f1
        metrics['sp_prec'] += sp_prec
        metrics['sp_recall'] += sp_recall

        # Retrieval evaluation (best recall across steps)
        max_step_recall = 0
        max_step_precision = 0
        for step_retrieved in item['recall_fact_id']:
            retrieved_set = set(step_retrieved)
            gold_set = set(item['supporting_id'])
            
            tp = len(retrieved_set & gold_set)
            fp = len(retrieved_set - gold_set)
            fn = len(gold_set - retrieved_set)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            if recall > max_step_recall:
                max_step_recall = recall
                max_step_precision = precision
        
        metrics['retrieval_recall'] += max_step_recall
        metrics['retrieval_precision'] += max_step_precision
        if max_step_precision + max_step_recall > 0:
            metrics['retrieval_f1'] += 2 * max_step_precision * max_step_recall / (max_step_precision + max_step_recall)

    # Average the metrics
    for key in metrics:
        if key != 'count':
            metrics[key] = round(metrics[key] / len(data) * 100, 2)
    
    return metrics


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


def f1_score(prediction, ground_truth):
    """Compute F1 score between prediction and ground truth."""
    normalized_prediction = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)

    ZERO_METRIC = (0, 0, 0)

    if normalized_prediction in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC
    if normalized_ground_truth in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC

    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return ZERO_METRIC
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, precision, recall


def normalize_sp(sps):
    """Normalize supporting facts for comparison."""
    new_sps = []
    for sp in sps:
        sp = list(sp)
        sp[0] = sp[0].lower()
        new_sps.append(sp)
    return new_sps

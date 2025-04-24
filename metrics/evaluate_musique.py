import string
import re
from collections import Counter

def evaluate_musique(data):
    """
    Evaluate MuSiQue predictions with the given data format.
    
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
        'answer_f1': 0,
        'answer_em': 0,
        'support_f1': 0,
        'support_em': 0,
        'retrieval_recall': 0,
        'retrieval_precision': 0,
        'retrieval_f1': 0,
        'count': len(data)
    }

    for item in data:
        # Answer evaluation
        max_em = 0
        max_f1 = 0
        for gold_answer in item['answer']:
            em = int(normalize_answer(item['prediction']) == normalize_answer(gold_answer))
            f1, _, _ = f1_score(item['prediction'], gold_answer)
            
            if em > max_em:
                max_em = em
            if f1 > max_f1:
                max_f1 = f1
        
        metrics['answer_em'] += max_em
        metrics['answer_f1'] += max_f1

        # Supporting facts evaluation
        predicted_support = list(set().union(*item['recall_fact_id']))
        gold_support = item['supporting_id']
        
        # Calculate supporting facts metrics
        tp = len(set(predicted_support) & set(gold_support))
        fp = len(set(predicted_support) - set(gold_support))
        fn = len(set(gold_support) - set(predicted_support))
        
        if tp + fp > 0:
            precision = tp / (tp + fp)
        else:
            precision = 0.0
            
        if tp + fn > 0:
            recall = tp / (tp + fn)
        else:
            recall = 0.0
            
        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0.0
            
        em = 1.0 if fp + fn == 0 else 0.0
        
        metrics['support_em'] += em
        metrics['support_f1'] += f1

        # Retrieval evaluation (best recall across steps)
        max_step_recall = 0
        max_step_precision = 0
        for step_retrieved in item['recall_fact_id']:
            retrieved_set = set(step_retrieved)
            gold_set = set(item['supporting_id'])
            
            tp = len(retrieved_set & gold_set)
            fp = len(retrieved_set - gold_set)
            fn = len(gold_set - retrieved_set)
            
            if tp + fp > 0:
                precision = tp / (tp + fp)
            else:
                precision = 0
                
            if tp + fn > 0:
                recall = tp / (tp + fn)
            else:
                recall = 0
                
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

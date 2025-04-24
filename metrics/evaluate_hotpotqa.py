import json
from typing import List, Dict, Any
import re
import string
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

def f1_score(prediction, ground_truth):
    """Calculate F1 score between prediction and ground truth."""
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

def exact_match_score(prediction, ground_truth):
    """Calculate exact match score."""
    return (normalize_answer(prediction) == normalize_answer(ground_truth))

def evaluate_hotpotqa(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Evaluate multi-hop QA performance based on the given data format.
    
    Args:
        data: List of dictionaries containing:
            - answer: List of ground truth answers (with aliases)
            - supporting_id: List of ground truth supporting fact IDs
            - recall_fact_id: List of lists containing retrieved fact IDs per hop
            - prediction: Model's predicted answer
    
    Returns:
        Dictionary containing various evaluation metrics
    """
    metrics = {
        'answer_em': 0,
        'answer_f1': 0,
        'answer_precision': 0,
        'answer_recall': 0,
        'supporting_fact_recall': 0,
        'supporting_fact_precision': 0,
        'supporting_fact_f1': 0,
        'retrieval_recall_per_hop': [],
        'retrieval_precision_per_hop': [],
        'retrieval_f1_per_hop': [],
        'joint_em': 0,
        'joint_f1': 0
    }
    
    total = len(data)
    if total == 0:
        return metrics
    
    # Initialize retrieval metrics for each hop
    max_hops = max(len(item['recall_fact_id']) for item in data) if data else 0
    retrieval_metrics_per_hop = [{'tp': 0, 'fp': 0, 'fn': 0} for _ in range(max_hops)]
    
    for item in data:
        # Answer evaluation (against all possible answer aliases)
        best_em = 0
        best_f1 = 0
        best_precision = 0
        best_recall = 0
        
        for gt_answer in item['answer']:
            em = exact_match_score(item['prediction'], gt_answer)
            f1, prec, recall = f1_score(item['prediction'], gt_answer)
            
            if f1 > best_f1:
                best_f1 = f1
                best_precision = prec
                best_recall = recall
                best_em = em
        
        metrics['answer_em'] += best_em
        metrics['answer_f1'] += best_f1
        metrics['answer_precision'] += best_precision
        metrics['answer_recall'] += best_recall
        
        # Supporting fact evaluation
        predicted_support = set()
        for hop_facts in item['recall_fact_id']:
            predicted_support.update(hop_facts)
        
        gt_support = set(item['supporting_id'])
        
        tp = len(predicted_support & gt_support)
        fp = len(predicted_support - gt_support)
        fn = len(gt_support - predicted_support)
        
        sp_precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        sp_recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        sp_f1 = 2 * sp_precision * sp_recall / (sp_precision + sp_recall) if (sp_precision + sp_recall) > 0 else 0
        
        metrics['supporting_fact_recall'] += sp_recall
        metrics['supporting_fact_precision'] += sp_precision
        metrics['supporting_fact_f1'] += sp_f1
        
        # Retrieval evaluation per hop
        for hop in range(len(item['recall_fact_id'])):
            hop_facts = set(item['recall_fact_id'][hop])
            tp = len(hop_facts & gt_support)
            fp = len(hop_facts - gt_support)
            fn = len(gt_support - hop_facts)
            
            retrieval_metrics_per_hop[hop]['tp'] += tp
            retrieval_metrics_per_hop[hop]['fp'] += fp
            retrieval_metrics_per_hop[hop]['fn'] += fn
        
        # Joint metrics
        joint_em = best_em * (1.0 if fp + fn == 0 else 0.0)
        joint_f1 = best_f1 * sp_f1
        
        metrics['joint_em'] += joint_em
        metrics['joint_f1'] += joint_f1
    
    # Normalize metrics
    for key in ['answer_em', 'answer_f1', 'answer_precision', 'answer_recall',
               'supporting_fact_recall', 'supporting_fact_precision', 'supporting_fact_f1',
               'joint_em', 'joint_f1']:
        metrics[key] /= total
    
    # Calculate retrieval metrics per hop
    for hop in range(max_hops):
        tp = retrieval_metrics_per_hop[hop]['tp']
        fp = retrieval_metrics_per_hop[hop]['fp']
        fn = retrieval_metrics_per_hop[hop]['fn']
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics['retrieval_recall_per_hop'].append(recall)
        metrics['retrieval_precision_per_hop'].append(precision)
        metrics['retrieval_f1_per_hop'].append(f1)
    
    return metrics

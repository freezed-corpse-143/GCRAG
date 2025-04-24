
import jsonlines
import argparse
from tqdm import tqdm



import heapq
from collections import defaultdict, deque
from typing import List, Tuple
from .entity_extractor import entity_extractor






def bipartite_gorder_sort(edges: List[Tuple[int, int]], window_size: int = 100) -> List[int]:
    """
    Sort the left partition of a bipartite graph to maximize common neighbors between adjacent vertices.
    Implementation based on GOrder algorithm from: https://github.com/datourat/Gorder
    
    Args:
        edges: List of edges as tuples (left_node, right_node)
        window_size: Size of sliding window to control locality of sorting
    
    Returns:
        Ordered list of left node IDs (preserving original IDs)
        Adjacency list mapping left nodes to their right neighbors
    """
    # Separate left and right partitions of the bipartite graph
    left_nodes = set()
    right_nodes = set()
    for u, v in edges:
        left_nodes.add(u)
        right_nodes.add(v)
    
    # Build adjacency lists for both directions
    left_to_right = defaultdict(set)  # Left partition → Right partition neighbors
    right_to_left = defaultdict(set)  # Right partition → Left partition neighbors
    
    for u, v in edges:
        left_to_right[u].add(v)
        right_to_left[v].add(u)
    
    left_nodes = list(left_nodes)
    left_degree = {u: len(neighbors) for u, neighbors in left_to_right.items()}
    
    # Initialize priority queue (using max-heap via negative values)
    heap = []
    node_priority = {}  # Tracks current priority of each node
    node_in_heap = {}    # Tracks whether node is in heap
    
    # Initial priority = negative degree (higher degree = higher priority)
    for u in left_nodes:
        priority = -left_degree[u]
        node_priority[u] = priority
        heapq.heappush(heap, (priority, u))
        node_in_heap[u] = True
    
    # Main sorting process
    order = []
    sliding_window = deque(maxlen=window_size)  # Tracks recently processed nodes
    
    while heap:
        # Get highest priority node (smallest negative value = largest degree)
        _, u = heapq.heappop(heap)
        if not node_in_heap.get(u, False):
            continue  # Skip if already processed
        
        order.append(u)
        node_in_heap[u] = False
        sliding_window.append(u)
        
        # Update priorities for nodes outside sliding window
        if len(sliding_window) == window_size:
            oldest_u = sliding_window.popleft()
            # Decrease priority of nodes sharing neighbors with oldest_u
            for v in left_to_right[oldest_u]:
                for neighbor_u in right_to_left[v]:
                    if neighbor_u != oldest_u and node_in_heap.get(neighbor_u, False):
                        # +1 to negative value = decrease priority
                        node_priority[neighbor_u] += 1  
                        heapq.heappush(heap, (node_priority[neighbor_u], neighbor_u))
        
        # Increase priority of nodes sharing neighbors with current node u
        for v in left_to_right[u]:
            for neighbor_u in right_to_left[v]:
                if neighbor_u != u and node_in_heap.get(neighbor_u, False):
                    # -1 to negative value = increase priority
                    node_priority[neighbor_u] -= 1  
                    heapq.heappush(heap, (node_priority[neighbor_u], neighbor_u))
    
    return order, left_to_right

def main():
    parser = argparse.ArgumentParser(description='Gorder for questions.')
    
    parser.add_argument('jsonl_path', 
                        type=str, 
                        help='path of jsonl')
    
    parser.add_argument('--sorted_key', 
                        type=str, 
                        default="question",
                        help='sorted key')
    
    args = parser.parse_args()



    with jsonlines.open(args.jsonl_path) as reader:
        data = list(reader)
    
    text_list = [ item[args.sorted_key] for item in data]
    text_list_len = len(text_list)
    

    entity_results = []
    entity_set = set()
    for text in tqdm(text_list, total=len(text_list)):
        entity_list = entity_extractor(text)
        entity_set.update(entity_list)
        entity_results.append(entity_list)
    
    entity_idx = {entity:(idx+text_list_len) for idx, entity in enumerate(entity_set)}

    edge_results = []
    for idx, entity_list in enumerate(entity_results):
        for entity in entity_list:
            edge_results.append((
                idx, entity_idx[entity]
            ))

    order, _ = bipartite_gorder_sort(edge_results)

    output_path = args.jsonl_path.replace(".jsonl", "_gorder_idx.txt")
    with open(output_path, 'w') as f:
        f.write("\n".join(map(str, order)))

if __name__ == "__main__":
    main()
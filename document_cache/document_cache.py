import numpy as np
import time
from .utils import text_encoder

class DocumentCache:
    def __init__(self, cache_capacity=500):
        self.cache_capacity = cache_capacity
        self.unique_documents = {}  # {id: {"id": str, "paragraph_text": str, "vector": np.array, "score": float, "last_accessed": float}}
        self.cooccurrence_matrix = np.eye(cache_capacity)  # Initialize as identity matrix
        self.id_to_index = {}  # Mapping from document id to matrix index
        self.index_to_id = {}  # Mapping from matrix index to document id
        self.next_index = 0  # Next available index in the matrix
        self.last_documents = []
        self.current_documents = []
        
    def add(self, documents):
        # Update document history
        self.last_documents = self.current_documents
        self.current_documents = documents
        
        # Find new documents not in cache
        new_docs = [doc for doc in documents if doc["id"] not in self.unique_documents]
        
        if new_docs:
            # Vectorize new documents
            for doc in new_docs:
                doc["vector"] = text_encoder(doc["paragraph_text"])
                doc["cache_score"] = 1.0  # Initial score
                doc["last_accessed"] = time.time()
            
            # Check if we need to make space
            while len(self.unique_documents) + len(new_docs) > self.cache_capacity:
                self._evict_lowest_scoring()
            
            # Add new documents to cache
            for doc in new_docs:
                self._add_document_to_cache(doc)
        
        # Update scores for accessed documents
        for doc in documents:
            if doc["id"] in self.unique_documents:
                cached_doc = self.unique_documents[doc["id"]]
                cached_doc["cache_score"] += 1  # Increase score on access
                cached_doc["last_accessed"] = time.time()
        
        # Update co-occurrence matrix if we have both last and current documents
        if self.last_documents and self.current_documents:
            self._update_cooccurrence_matrix()
    
    def _add_document_to_cache(self, document):
        # Assign the next available index
        if self.next_index < self.cache_capacity:
            index = self.next_index
            self.next_index += 1
        else:
            # Find an index that's no longer in use (shouldn't happen if eviction works correctly)
            used_indices = set(self.id_to_index.values())
            for i in range(self.cache_capacity):
                if i not in used_indices:
                    index = i
                    break
        
        # Add the document to cache
        doc_id = document["id"]
        self.unique_documents[doc_id] = {
            "id": doc_id,
            "paragraph_text": document["paragraph_text"],
            "vector": document["vector"],
            "cache_score": document["cache_score"],
            "last_accessed": document["last_accessed"]
        }
        
        # Update mappings
        self.id_to_index[doc_id] = index
        self.index_to_id[index] = doc_id
    
    def _evict_lowest_scoring(self):
        if not self.unique_documents:
            return
        
        # Apply score decay based on time since last access
        current_time = time.time()
        for doc in self.unique_documents.values():
            time_since_access = current_time - doc["last_accessed"]
            doc["cache_score"] *= max(0, 1 - 0.01 * time_since_access)  # Decay factor
        
        # Find document with lowest score
        lowest_score = float('inf')
        evict_id = None
        for doc_id, doc in self.unique_documents.items():
            if doc["cache_score"] < lowest_score:
                lowest_score = doc["cache_score"]
                evict_id = doc_id
        
        if evict_id:
            # Remove from cache and mappings
            index = self.id_to_index[evict_id]
            del self.unique_documents[evict_id]
            del self.id_to_index[evict_id]
            del self.index_to_id[index]
    
    def _update_cooccurrence_matrix(self):
        # Get all valid document pairs between last and current documents
        for last_doc in self.last_documents:
            if last_doc["id"] not in self.id_to_index:
                continue  # Skip if not in cache
            
            i = self.id_to_index[last_doc["id"]]
            
            for current_doc in self.current_documents:
                if current_doc["id"] not in self.id_to_index:
                    continue  # Skip if not in cache
                
                j = self.id_to_index[current_doc["id"]]
                
                # Increment co-occurrence count
                self.cooccurrence_matrix[i][j] += 1
    
    def get_document_score(self, doc_id):
        if doc_id in self.unique_documents:
            return self.unique_documents[doc_id]["cache_score"]
        return 0
    
    def get_cooccurrence_count(self, doc_id1, doc_id2):
        if doc_id1 in self.id_to_index and doc_id2 in self.id_to_index:
            i = self.id_to_index[doc_id1]
            j = self.id_to_index[doc_id2]
            return self.cooccurrence_matrix[i][j]
        return 0

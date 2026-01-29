"""Vector Store - Pure Python (Instant)"""
import re

class VectorStore:
    def __init__(self):
        self.documents = []
        self.is_initialized = False

    def tokenize(self, text):
        """Simple tokenizer"""
        return set(re.findall(r'\w+', text.lower()))

    def build_index(self, documents):
        """Build simple index"""
        if not documents:
            raise ValueError("No documents")
        self.documents = documents
        for doc in self.documents:
            doc['tokens'] = self.tokenize(doc['text'])
        self.is_initialized = True
        print(f"Indexed {len(documents)} chunks")

    def search(self, query, top_k=5):
        """Jaccard similarity search"""
        if not self.is_initialized:
            return []
            
        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []
            
        scores = []
        for doc in self.documents:
            doc_tokens = doc['tokens']
            intersection = len(query_tokens & doc_tokens)
            union = len(query_tokens | doc_tokens)
            score = intersection / union if union > 0 else 0
            if score > 0:
                scores.append({"text": doc['text'], "score": score})
        
        # Sort by score descending
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:top_k]

    def clear(self):
        self.documents = []
        self.is_initialized = False
    
    def get_count(self):
        return len(self.documents)

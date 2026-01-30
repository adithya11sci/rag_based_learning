"""RAG Engine - Fast & Stable with Token Optimization"""
import os
import hashlib
from dotenv import load_dotenv
from groq import Groq
from .pdf_processor import PDFProcessor
from .vector_store import VectorStore

load_dotenv()

class RAGEngine:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.vector_store = VectorStore()
        
        api_key = os.getenv("GROQ_API_KEY")
        self.groq = Groq(api_key=api_key) if api_key else None
        self.pdf_name = None
        
        # Cache for responses (saves API tokens!)
        self.cache = {}
        self.max_cache_size = 50
        
        if not api_key:
            print("Warning: GROQ_API_KEY not set!")
    
    def _get_cache_key(self, query, context_hash):
        """Generate cache key from query and context"""
        return hashlib.md5(f"{query}:{context_hash}".encode()).hexdigest()
    
    def process_pdf(self, pdf_path, pdf_name):
        try:
            chunks = self.pdf_processor.process_pdf(pdf_path)
            self.vector_store.build_index(chunks)
            self.pdf_name = pdf_name
            # Clear cache when new PDF is uploaded
            self.cache = {}
            return {
                "success": True, 
                "message": f"Processed {pdf_name}", 
                "chunk_count": len(chunks),
                "total_characters": sum(c['char_count'] for c in chunks)
            }
        except Exception as e:
            return {"success": False, "message": str(e), "chunk_count": 0}
            
    def ask(self, query):
        if not self.vector_store.is_initialized:
            return {"success": False, "answer": "Please upload a PDF first."}
            
        results = self.vector_store.search(query, top_k=5)
        
        # If no results but we have documents, use available content
        if not results and self.vector_store.get_count() > 0:
            all_docs = self.vector_store.documents[:3]
            results = [{"text": d['text'], "score": 0.1} for d in all_docs]
            
        if not results:
            return {"success": False, "answer": "No content available. Please upload a PDF."}
            
        context_text = "\n".join([r['text'] for r in results])
        
        # Check cache first (saves API tokens!)
        context_hash = hashlib.md5(context_text.encode()).hexdigest()[:8]
        cache_key = self._get_cache_key(query.lower().strip(), context_hash)
        
        if cache_key in self.cache:
            return {"success": True, "answer": self.cache[cache_key], "cached": True}
        
        if not self.groq:
            return {"success": False, "answer": "Groq API key missing."}
            
        try:
            response = self.groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer based only on the provided context."},
                    {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
                ],
                temperature=0.3,
                max_tokens=1024
            )
            answer = response.choices[0].message.content
            
            # Cache the response
            if len(self.cache) >= self.max_cache_size:
                # Remove oldest entry
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            self.cache[cache_key] = answer
            
            return {"success": True, "answer": answer, "context": results}
        except Exception as e:
            return {"success": False, "answer": f"Error: {str(e)}"}
            
    def get_status(self):
        return {
            "has_document": self.vector_store.is_initialized,
            "pdf_name": self.pdf_name,
            "chunk_count": self.vector_store.get_count()
        }
        
    def clear(self):
        self.vector_store.clear()
        self.pdf_name = None
        self.cache = {}

"""RAG Engine - Fast & Stable"""
import os
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
        
        if not api_key:
            print("Warning: GROQ_API_KEY not set!")
    
    def process_pdf(self, pdf_path, pdf_name):
        try:
            chunks = self.pdf_processor.process_pdf(pdf_path)
            self.vector_store.build_index(chunks)
            self.pdf_name = pdf_name
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
        
        # If no results but we have documents, use all available content
        if not results and self.vector_store.get_count() > 0:
            # Fallback: use first chunk
            all_docs = self.vector_store.documents[:3]
            results = [{"text": d['text'], "score": 0.1} for d in all_docs]
            
        if not results:
            return {"success": False, "answer": "No content available. Please upload a PDF."}
            
        context_text = "\n\n".join([f"{r['text']}" for r in results])
        
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
            return {"success": True, "answer": response.choices[0].message.content, "context": results}
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

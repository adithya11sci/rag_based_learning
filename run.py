"""Run the RAG Learning Assistant"""
import uvicorn

if __name__ == "__main__":
    print("\n🎓 RAG Learning Assistant")
    print("📍 Open http://localhost:8000\n")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

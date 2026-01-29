# 🎓 RAG Learning Assistant

> A powerful, instant AI learning companion that lets you chat with your PDF study materials.

![RAG Badge](https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-Llama3-orange?style=for-the-badge)

Upload any PDF textbook, research paper, or notes, and ask questions instantly. The system uses **Retrieval-Augmented Generation (RAG)** to provide accurate answers based strictly on your document's content.

## ✨ Features

- **🚀 Instant Processing**: Uses a custom Pure Python vector engine (Zero-Lag)
- **🧠 Smart Answers**: Powered by Llama 3 (via Groq API) for high-quality explanations
- **⚡ Super Fast**: No heavy machine learning dependencies installation required
- **🎨 Premium UI**: Beautiful dark-mode interface with smooth animations
- **📱 Responsive**: Works great on desktop and mobile

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI Engine**: Groq API (Llama 3.3 70B)
- **Vector Store**: Custom In-Memory Store (Jaccard/TF-IDF) - *Blazing Fast*
- **Frontend**: Vanilla JS + CSS3 (Glassmorphism Design)

## 🚀 Quick Start

### 1. Clone the Repo
```bash
git clone https://github.com/adithya11sci/rag_based_learning.git
cd rag_based_learning
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```
*(Get a free key from console.groq.com)*

### 4. Run the App
```bash
python run.py
```
Open **http://localhost:8000** in your browser!

## 📸 Screenshots

*(Add screenshots of your UI here)*

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit PRs.

## 📄 License

MIT License © 2024

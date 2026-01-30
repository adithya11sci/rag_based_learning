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

## 🌐 Live Demo

🚀 **Try it now**: [https://rag-based-learning.onrender.com](https://rag-based-learning.onrender.com)

## 🌐 Free Deployment (Render.com)

Deploy your own instance completely **FREE** with **24/7 uptime**!

### One-Click Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/adithya11sci/rag_based_learning)

### Manual Deploy Steps

1. **Create a Render Account**: Go to [render.com](https://render.com) and sign up for free

2. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select the `rag_based_learning` repository

3. **Configure the Service**:
   | Setting | Value |
   |---------|-------|
   | Name | `rag-learning-assistant` |
   | Environment | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |
   | Instance Type | `Free` |

4. **Add Environment Variable**:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key (get free at [console.groq.com](https://console.groq.com))

5. **Deploy!** Click "Create Web Service" and wait ~2-3 minutes

Your app will be live at: `https://rag-learning-assistant.onrender.com`

### 🔄 24/7 Uptime (Free)

This app uses automatic health checks via [cron-job.org](https://cron-job.org) to stay awake 24/7:

- **Health endpoint**: `/api/health` is pinged every 14 minutes
- **No sleep mode**: App stays active and responsive
- **Zero cost**: Both Render and cron-job.org are free!

🔗 **Live Demo**: [https://rag-based-learning.onrender.com](https://rag-based-learning.onrender.com)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit PRs.

## 📄 License

MIT License © 2024

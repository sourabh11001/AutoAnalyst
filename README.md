# 🤖 AutoAnalyst Pro  

> Your AI Data Consultant. Upload datasets, ask complex questions, and generate enterprise-grade reports in seconds.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)

---

## 📖 Overview

AutoAnalyst Pro is a full-stack AI-powered data analysis platform that converts raw CSV/Excel datasets into actionable insights.  
Unlike traditional dashboards, it uses **active reasoning** to think through problems, generate Python analysis code, create visualizations, train machine learning models, and explain results in natural language.

It bridges the gap between **technical data science** and **business decision-making**, acting like an AI consultant that explains not only *what* is happening but also *why* it is happening.

---

## ✨ Key Features

- 🧠 **Cognitive AI Engine** powered by Gemini 2.5 Flash  
- 🔮 **AutoML Engine** for predictive modeling (Random Forest, etc.)  
- 📊 **Dynamic Visualizations** (Bar, Line, Pie, Scatter)  
- 📄 **Consultant-Grade PDF Reports** with KPIs & summaries  
- ⚡ **High-Performance Backend** built using FastAPI  
- 🎨 **Enterprise UI** with Tailwind CSS & glassmorphism design  
- 📁 Drag-and-drop CSV upload  
- 🧪 Works on real-world datasets like Sales, Titanic, Finance, Marketing  

---

## 🛠 Tech Stack

- **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS, Chart.js  
- **Backend:** Python, FastAPI, Uvicorn  
- **Data Science:** Pandas, NumPy, Scikit-Learn  
- **Visualization:** Matplotlib, Seaborn (PDF), Chart.js (Web)  
- **AI/LLM:** Google Generative AI (Gemini 2.5 Flash)  
- **Reporting:** FPDF  

---

## 🏗 Architecture

```
Frontend (HTML + JS)
        ↓
FastAPI Backend
        ↓
Data Processing (Pandas + ML)
        ↓
Gemini 2.5 Flash (Reasoning + Code Generation)
        ↓
Charts + PDF Reports
```

This mirrors real-world AI analytics systems used in enterprise environments.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/sourabh11001/AutoAnalyst.git
cd AutoAnalyst
```

---

### 2. Create Virtual Environment
```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

### 3. Install Dependencies
```bash
pip install fastapi uvicorn pandas numpy scikit-learn python-multipart google-generativeai python-dotenv fpdf matplotlib seaborn
```

---

### 4. Configure API Key

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

### 5. Run the Server
```bash
python -m backend.main
```

Open in browser:
```
http://127.0.0.1:8000
```

---

## 💡 How to Use

1. Upload a CSV file (e.g., `titanic.csv`, `sales_data.csv`)  
2. The AI automatically:
   - Generates an Executive Summary  
   - Suggests analytical questions  
3. Ask queries like:
   - "Show a scatter plot of Age vs Fare"  
   - "Train a model to predict Profit"  
   - "Why did sales drop in Q3?"  
4. Click **Export PDF Report** to download a full professional report.

---

## 📸 Screenshots

(Add your screenshots here)

---

## 📈 Why This Project Is Strong

This project demonstrates:

- Real-world AI system design  
- AutoML pipelines  
- AI-driven reasoning over data  
- Production-style FastAPI backend  
- Consultant-style reporting automation  
- Enterprise UI thinking  

This is **portfolio-grade** and **interview-grade**.

---

## 🤝 Contributing

Contributions are welcome.  
Feel free to submit pull requests to enhance UI, ML models, or reporting.

---

## 📄 License

This project is licensed under the MIT License.

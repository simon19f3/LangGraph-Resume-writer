# 🧠 Smart Resume & Job Application Agent  
**LangGraph + Ollama + Gradio**

This project is an intelligent, context-aware job application assistant.  
It automatically generates:

- 📄 Resumes  
- ✉️ Cover Letters  
- 🎤 Interview Screening Answers  

The system uses **LangGraph** for workflow orchestration and **Ollama** for local LLM inference.  
You can paste any job description — the agent filters your skills (AI, frontend, or both)  
and produces tailored content.

---

## 🚀 Features
### ✓ Intelligent Skill Filtering
The agent decides if the job is:
- AI-related  
- Frontend-related  
- Hybrid  

Then filters your profile so the LLM **only** sees relevant skills.

### ✓ LangGraph Workflow
Nodes:
- Profile Collector  
- Job Analyzer  
- Conditional Router  
- Resume Generator  
- Cover Letter Generator  
- Screening Q/A Generator  

### ✓ Fully Modular Codebase
Code is split into:
```
state/        # State definitions
nodes/        # Each graph node
llm/          # LLM configuration
utils/        # Helpers (optional)
graph.py      # Builds and compiles the LangGraph graph
app.py        # Gradio UI interface
```

---

## 📦 Install & Run

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Install & Start Ollama  
Download: https://ollama.com  

Then pull a model:
```bash
ollama pull llama3.2
```

Make sure Ollama is running:
```bash
ollama serve
```

---

## ▶️ Launch the App
```bash
python app.py
```

Gradio will start at:
```
http://127.0.0.1:7860
```

---

## 🐳 Run Using Docker

### Build the image:
```bash
docker build -t smart-resume-agent .
```

### Run the container:
> ⚠️ Ollama must be installed on the host and mounted into Docker

```bash
docker run -it --net=host \
  -v ~/.ollama:/root/.ollama \
  smart-resume-agent
```

---



## 🧪 Testing Your Graph Node-by-Node
You can test a workflow step manually:

```python
from graph import build_graph
workflow = build_graph()

workflow.invoke({"messages": [{"role": "user", "content": "Resume for AI engineer"}]})
```

---

## 🤝 Contributing
Pull requests are welcome!  
Please format code with **Black** and follow the modular structure.

---

## 📝 License
MIT License.

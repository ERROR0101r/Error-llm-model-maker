
# 🤖 DESI LLM - Pure Python Language Model Maker

### Train Your Own LLM on Android/Linux - Zero Dependencies

<div align="center">
  <img src="https://img.shields.io/badge/Total%20Files-7-FF0000?style=for-the-badge">
  <img src="https://img.shields.io/badge/Dependencies-Zero-00FF00?style=for-the-badge">
  <img src="https://img.shields.io/badge/Platform-Android%20%7C%20Linux-FF6600?style=for-the-badge">
  <img src="https://img.shields.io/badge/Parameters-Up%20to%201.3M-FF00FF?style=for-the-badge">
  
  [![Telegram](https://img.shields.io/badge/Telegram-@ERROR0101risback-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/ERROR0101risback)
  [![GitHub](https://img.shields.io/badge/GitHub-ERROR0101r-181717?style=for-the-badge&logo=github)](https://github.com/ERROR0101r)
  
  <p><strong>Developer: @ERROR0101risback</strong></p>
  <p><em>No numpy, no pytorch, no tensorflow - Pure Python</em></p>
</div>

---

## 📋 WHAT IS DESI LLM?

**Desi LLM** is a complete framework to **train and run your own Language Model** on your phone or laptop. Uses only Python built-in libraries.

| # | File | Purpose | Status |
|---|------|---------|--------|
| 1 | **llm_core.py** | Core model logic (word-level n-gram) | ✅ WORKING |
| 2 | **trainer.py** | Train model from folder of text files | ✅ WORKING |
| 3 | **chat.py** | Interactive chat with context memory | ✅ WORKING |
| 4 | **api.py** | REST API server + Web UI | ✅ WORKING |
| 5 | **clean_data.py** | Remove garbage from training data | ✅ WORKING |
| 6 | **data.py** | Data utilities | ✅ WORKING |
| 7 | **Data/** | Folder for your .txt training files | ✅ WORKING |

---

## 🚀 HOW TO USE

### Step 1: Train Your Model

```bash
python trainer.py
# Enter model name: my_ai
# Enter folder path: Data
# Output: Model saved to saved_models/my_ai.json
```

Step 2: Chat With Your Model

```bash
python chat.py
# Select model: my_ai
# You: hello
# 🤖: Hello how are you?
```

Step 3: Start API Server

```bash
python api.py
# Open browser: http://localhost:8000
```

---

📡 API ENDPOINTS

Method Endpoint Description
GET /api/models List all trained models
GET /api/load?name=MODEL Load a model
GET /api/generate?seed=TEXT&words=50 Generate text

Example API Calls

List Models

```bash
curl http://localhost:8000/api/models
```

Load Model

```bash
curl "http://localhost:8000/api/load?name=my_ai"
```

Generate Text

```bash
curl "http://localhost:8000/api/generate?seed=hello%20how%20are%20you&words=50&temp=0.5"
```

---

💻 PYTHON USAGE

```python
import requests

# Load model
requests.get("http://localhost:8000/api/load?name=my_ai")

# Generate text
response = requests.get(
    "http://localhost:8000/api/generate",
    params={"seed": "hello", "words": 50, "temp": 0.5}
)
print(response.json()['generated'])
```

---

📁 TRAINING DATA FORMAT

· Put any .txt files in Data/ folder
· Model learns word by word from all files
· Supports any language (English, Hindi, etc.)

Example training file:

```
Hello. Hi there. How are you. I am fine. Good to see you. 
Nice to meet you. Have a great day. Goodbye. See you later.
```

---

🎯 FEATURES

Feature Description
Word-level generation No character garbage
Context memory Remembers last 3 exchanges
Quality filter Auto-retry on bad responses
Temperature control 0.3=focused, 1.0=creative
Multi-model support Train multiple models
Zero dependencies Built-in Python only

---

🔧 SYSTEM REQUIREMENTS

Requirement Minimum
Python 3.6+
RAM 256MB
Storage 20MB per model
Platform Android (Termux), Linux, Windows

---

📁 COMPLETE FILE STRUCTURE

```
Error-llm-model-maker/
├── llm_core.py
├── trainer.py
├── chat.py
├── api.py
├── clean_data.py
├── data.py
├── Data/
│   ├── conversation.txt
│   ├── stories.txt
│   └── your_files.txt
└── saved_models/
    └── my_ai.json
```

---

📞 DEVELOPER CONTACT

<div align="center">
  <p><strong>Name:</strong> ERROR</p>
  <p>
    <a href="https://t.me/ERROR0101risback">Telegram</a> •
    <a href="https://github.com/ERROR0101r">GitHub</a>
  </p>
  <p><strong>Email:</strong> t1342095@gmail.com</p>
</div>

---

🔗 REPOSITORY

· GitHub: https://github.com/ERROR0101r/Error-llm-model-maker

---

📜 LICENSE

```
Free to use, modify, and share.
Credit appreciated but not required.

© 2026 Desi LLM | Developed by ERROR
```

---

<div align="center">
  <h3>🤖 Train Your Own LLM Today 🤖</h3>
  <p><i>No GPU. No Cloud. No Dependencies.</i></p>
  <p><i>Just Pure Python.</i></p>

  <p>
    <a href="https://t.me/ERROR0101risback"><img src="https://img.shields.io/badge/Telegram-@ERROR0101risback-26A5E4?style=flat-square&logo=telegram"></a>
    <a href="https://github.com/ERROR0101r"><img src="https://img.shields.io/badge/GitHub-ERROR0101r-181717?style=flat-square&logo=github"></a>
  </p>

  <p><strong>⭐ Star this repo if you find it useful! ⭐</strong></p>
</div>
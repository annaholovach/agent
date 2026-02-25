# Lightweight autonomous AI agent with:

    - Streamlit UI
    - Chroma vector database
    - Ollama LLM
    - Web search tool
    - To-do tools

# Install Dependencies
1. Create virtual environment
```Bash
python -m venv venv
```

2. Activate it:
Windows
```Bash
venv\Scripts\activate
```
Mac/Linux:
```Bash
source venv/bin/activate
```

3. Install Python dependencies
```Bash
pip install -r requirements.in
```

4. Pull Ollama Model
```Bash
ollama pull llama3
```

5. Run Chroma in Docker
```Bash
docker-compose up -d
```

6. Run the App
```Bash
streamlit run app.py
```

# Requirements

    - Python 3.11+
    - Docker
    - Ollama

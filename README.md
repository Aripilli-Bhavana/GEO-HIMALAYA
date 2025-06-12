Here is the **complete Python code** for a `readme_generator.py` script that generates the final `README.md` file for your **GEO-HIMALAYA** project, based on your exact structure and workflow.

---

### ✅ `readme_generator.py`

```python
readme_content = """
# GEO-HIMALAYA 🌄

GEO-HIMALAYA is a geospatially-aware chatbot assistant tailored for Uttarakhand-based GIS vector datasets. It leverages LangChain + Ollama to answer user queries with intelligent metadata matching and SQL generation for AOI-specific analysis.

🚀 **Live Demo Integration**: [maps.iirs.gov.in](https://maps.iirs.gov.in)

---

## 📁 Project Structure

```

GEO-HIMALAYA/
├── conf/
│   └── server.conf              # Contains LLM host and port
├── metadata/
│   └── metadata.json            # Metadata of all GIS datasets
├── matcher/
│   └── matcher.py               # Logic for metadata-based keyword matching
├── helper/
│   └── prompt\_helper.py        # Builds prompt for LLM using metadata
├── llm/
│   └── **init**.py             # Makes requests to Ollama server via LangChain
├── server/
│   ├── routes.py               # API routes (Flask blueprint)
│   └── templates/, static/     # HTML + JS assets (if web front-end is used)
├── src/
│   └── main.py                 # CLI interface for chatbot
├── run-docker.sh               # Run Ollama in Docker
├── run-native.sh               # Native run script for Linux/macOS
├── run-ative.ps1              # Native run script for Windows
└── requirements.txt            # Python dependencies

````

---

## ⚙️ How It Works

### 🔗 Connection to Ollama LLM

- Ollama server is hosted on the main machine with IP and port defined in `conf/server.conf`:

```ini
[llm]
host = 172.16.30.215
port = 11434
````

* The Python app running locally reads this config and connects via:

```python
LLM_URL = f"http://{host}:{port}/api/chat"
```

* You can switch between `llama3:latest` or `mistral:latest` models dynamically from code.

---

### 🧠 Query Flow

1. **User Input**:

   * CLI/Flask frontend takes natural language input.
2. **Metadata Matcher**:

   * Uses `matcher.py` to extract relevant dataset context from `metadata.json`.
3. **Prompt Generator**:

   * Builds a system prompt using `prompt_helper.py`, containing:

     * Matching tables
     * Schema details
     * Examples and strict rules
4. **LLM Call**:

   * Sends prompt to `Ollama` with `POST /api/chat`.
   * Receives SQL query and a summary.
5. **Response**:

   * Prints result in this format:

     ```
     LLM Response: Roads include National highway, Village road...
     View Operation:
     SELECT roads.gid, ...
     ```

---

## 🧪 Running the Project

### 1. Install Ollama and models

* On main server:

```bash
ollama serve
ollama run mistral
ollama run llama3
```

### 2. Local Setup (Windows/Linux/macOS)

#### a. Using `run-ative.ps1` (Windows):

```powershell
./run-ative.ps1
```

#### b. Using `run-native.sh` (Linux/macOS):

```bash
chmod +x run-native.sh
./run-native.sh
```

#### c. Using Docker:

```bash
./run-docker.sh
```

---

## 🌐 Integration with maps.iirs.gov.in

* This chatbot runs as a backend or CLI module that processes queries.
* **maps.iirs.gov.in** handles the spatial interface and shapefile inputs.
* GEO-HIMALAYA receives the Area of Interest (AOI) and question from the frontend.
* It returns a summary and SQL query which can be used to fetch/post-process layers on the map.

---

## 🧠 Technologies Used

* Python 3.10+
* Flask
* LangChain
* Ollama (LLaMA3, Mistral)
* PostGIS
* Metadata-driven prompt engineering

---

## ✅ Status

* [x] AOI-based querying
* [x] Strict SQL generation with context
* [x] Ollama model switching
* [x] GitHub-ready structure
  """

# Write to file

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme\_content.strip())

print("✅ README.md generated successfully.")

````

---

### ✅ How to Use

1. Save the script as `readme_generator.py` in your project root.
2. Run it:

```bash
python readme_generator.py
````


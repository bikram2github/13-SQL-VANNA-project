```markdown
# 🧠 SQL AI Agent (Vanna + FastAPI + SQLite)

An AI-powered SQL assistant that converts natural language questions into SQL queries, executes them on a SQLite database, and returns structured answers with optional visualizations.

---

## 🚀 Features

- 🔍 Natural Language → SQL Query generation
- 🧠 Memory-based learning (improves over time)
- 📊 Data visualization support (Plotly)
- 🛡️ SQL validation for safety (only SELECT allowed)
- ⚡ FastAPI backend with chat interface
- 🗄️ SQLite database with realistic healthcare dataset

---

## 🏗️ Project Structure

```

├── main.py                 # FastAPI app entry point
├── vanna_setup.py         # Agent + LLM + tools setup
├── sql_validator.py       # SQL safety validation
├── setup_database.py      # Database creation & seeding
├── seed_memory.py         # Train agent memory
├── clinic.db              # SQLite database
├── requirements.txt       # Dependencies
├── RESULTS.md             # Test results
└── README.md              # Documentation

````

---

## ⚙️ Tech Stack

- **Backend:** FastAPI
- **LLM:** Groq (OpenAI-compatible API)
- **Agent Framework:** Vanna AI
- **Database:** SQLite
- **Visualization:** Plotly
- **Language:** Python 3.10+

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
````

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

📄 Dependencies: 

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

⚠️ Required for LLM access.

---

## 🗄️ Setup Database

Run the script to create and populate the database:

```bash
python setup_database.py
```

This will:

* Create tables (patients, doctors, appointments, etc.)
* Insert realistic sample data

📄 See: 

---

## 🧠 Train Agent Memory (Optional but Recommended)

```bash
python seed_memory.py
```

This helps the agent learn common queries for better accuracy.

📄 See: 

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

Server will start at:

👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔗 Available Endpoints

### ✅ Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

### 💬 Chat Interface

Vanna chat routes are auto-registered:

* `/chat`
* `/ask`
* `/run_sql`

📄 Defined in: 

---

## 🛡️ SQL Safety

All queries are validated before execution:

* ❌ No INSERT, UPDATE, DELETE
* ❌ No system table access
* ✅ Only SELECT queries allowed

📄 See: 

---

## 🧪 Test Results

📄 See full results: 

**Summary:**

* Total Questions: 20
* Passed: 18 ✅
* Partial: 1 ⚠️
* Failed: 1 ❌

---

## 🧠 Example Query

**Input:**

```
How many patients do we have?
```

**Output:**

```
SQL: SELECT COUNT(*) FROM patients;

Explanation: Counts total number of patients.

Answer: 200
```

---

## ⚠️ Known Limitations

* Some complex joins may produce unformatted output
* Visualization depends on structured data
* Requires API key (no offline mode)

---

## 💡 Future Improvements

* ✅ Better response formatting
* 📈 Improved chart generation
* ⚡ Query caching
* 🧠 Smarter memory retrieval
* 🌐 Frontend UI integration


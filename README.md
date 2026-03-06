# 🌍 Country Information AI Agent

An AI-powered agent that answers questions about countries using the **REST Countries API**.
The system is built using **FastAPI** and **LangGraph** to create a structured agent workflow that processes user queries, identifies the requested information, retrieves data from the API, and generates a human-readable response.

---

# 📌 Features

* Query country information using natural language
* Extracts **country name** and **requested fields**
* Uses **LangGraph agent workflow**
* Fetches live data from **REST Countries API**
* Returns structured responses with confidence score
* FastAPI REST endpoint
* Deployable to cloud platforms (Render / Railway / AWS)

---

# 🏗️ System Architecture

The agent follows a **multi-step workflow using LangGraph**.

```
User Query
   │
   ▼
Intent Detection
(Identify country & fields)
   │
   ▼
API Tool Call
(REST Countries API)
   │
   ▼
Answer Synthesis
   │
   ▼
Final Response
```

Each step is implemented as a **LangGraph node**.

---

# ⚙️ Tech Stack

| Component       | Technology         |
| --------------- | ------------------ |
| API Framework   | FastAPI            |
| Agent Workflow  | LangGraph          |
| HTTP Requests   | httpx              |
| Data Validation | Pydantic           |
| Server          | Uvicorn            |
| External API    | REST Countries API |

---

# 📂 Project Structure

```
country-ai-agent/
│
├── main.py
|___helpers.py
|__models.py
|__state.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🔌 Data Source

The system uses the public API:

https://restcountries.com

Example endpoint:

```
https://restcountries.com/v3.1/name/{country}
```

Example:

```
https://restcountries.com/v3.1/name/germany
```

---

# 🚀 Running the Project Locally

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/country_agent.git
cd country_agent
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## 4️⃣ Run the Application

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://localhost:8000
```

---

# 🧪 API Usage

## Swagger UI

```
http://localhost:8000/docs
```

---

## Endpoint

```
POST /ask
```

### Request Body

```json
{
  "query": "What is the population of Germany?"
}
```

---

### Example Response

```json
{
  "answer": "Germany's population is 83,240,525.",
  "country": "Germany",
  "fields": ["population"],
  "confidence": 0.95,
  "source": "REST Countries API"
}
```

---

# 💡 Example Queries

```
What is the population of Germany?
```

```
What currency does Japan use?
```

```
What is the capital of India?
```

```
What are the languages spoken in Canada?
```

---

# 🔁 Agent Workflow (LangGraph)

The system uses **LangGraph StateGraph** to control execution flow.

### Nodes

| Node              | Function                             |
| ----------------- | ------------------------------------ |
| intent_router     | Extract country and requested fields |
| api_caller        | Call REST Countries API              |
| synthesize_answer | Generate response                    |
| error_handler     | Handle errors                        |

### Execution Flow

```
Intent Detection
      ↓
API Call
      ↓
Success → Answer Synthesizer
Failure → Error Handler
```

---

## 🌐 Live Deployment

The application is deployed on **Render**.

**Application URL**

https://country-agent.onrender.com

**Swagger API Documentation**

https://country-agent.onrender.com/docs


# ⚠️ Limitations

* Country detection uses **regex-based heuristics**
* Only supports limited fields:

  * population
  * capital
  * currency
  * languages
  * area
  * region
* No support for **multi-country queries**
* Does not use an LLM for advanced reasoning

---

# 🚀 Future Improvements

Possible enhancements:

* Add **LLM-based intent detection**
* Support more country attributes
* Add **caching layer**
* Add **vector search for country knowledge**
* Improve entity extraction
* Add **multi-language support**

---

# 🧑‍💻 Author

Ponnapula Gangothri

Software Developer | AI Engineer

---

# 📜 License

This project is open-source and available under the **MIT License**.

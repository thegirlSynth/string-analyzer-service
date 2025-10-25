
# 🧩 String Analyzer Service (Stage 1)

A simple yet powerful **RESTful API** built with **FastAPI** that analyzes strings and stores their computed properties.
This service forms the foundation of a multi-stage backend engineering challenge.

---

## 🚀 Features

For each analyzed string, the service computes and stores:

| Property | Description |
|-----------|--------------|
| `length` | Number of characters in the string |
| `is_palindrome` | Whether the string reads the same backward and forward (case-insensitive) |
| `unique_characters` | Count of distinct characters in the string |
| `word_count` | Number of words separated by whitespace |
| `sha256_hash` | SHA-256 hash of the string for unique identification |
| `character_frequency_map` | Dictionary mapping each character to its occurrence count |

---

## 🧠 Endpoints Overview

### 1️⃣ Create / Analyze String
**POST** `/strings`

Analyzes and stores a string.

#### Request
```json
{
  "value": "madam racecar level"
}
````

#### Success (201 Created)

```json
{
  "id": "e3b0c44298...",
  "value": "madam racecar level",
  "properties": {
    "length": 18,
    "is_palindrome": false,
    "unique_characters": 9,
    "word_count": 3,
    "sha256_hash": "e3b0c44298...",
    "character_frequency_map": {
      "m": 2,
      "a": 4,
      " ": 2,
      "r": 2,
      "c": 1,
      "e": 2,
      "l": 2,
      "v": 1
    }
  },
  "created_at": "2025-10-25T22:31:00Z"
}
```

#### Error Responses

| Status | Description                                    |
| ------ | ---------------------------------------------- |
| 400    | Invalid request body or missing `value`        |
| 409    | String already exists in the system            |
| 422    | Invalid data type for `value` (must be string) |

---

### 2️⃣ Get Specific String

**GET** `/strings/{string_value}`

Retrieve analysis details for a specific string.

#### Success (200 OK)

```json
{
  "id": "e3b0c44298...",
  "value": "madam",
  "properties": { ... },
  "created_at": "2025-10-25T22:31:00Z"
}
```

#### Error

| Status | Description                         |
| ------ | ----------------------------------- |
| 404    | String does not exist in the system |

---

### 3️⃣ Get All Strings (Filtered)

**GET** `/strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a`

Filter previously analyzed strings by multiple parameters.

#### Example Success (200 OK)

```json
{
  "data": [
    {
      "id": "hash1",
      "value": "racecar level",
      "properties": { ... },
      "created_at": "2025-10-25T22:31:00Z"
    }
  ],
  "count": 1,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "max_length": 20,
    "word_count": 2,
    "contains_character": "a"
  }
}
```

#### Error

| Status | Description                             |
| ------ | --------------------------------------- |
| 400    | Invalid query parameter values or types |

---

### 4️⃣ Natural Language Filtering

**GET** `/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings`

Query the system using **simple natural language**.

#### Example Query

```
/strings/filter-by-natural-language?query=all single word palindromic strings
```

#### Example Response (200 OK)

```json
{
  "data": [ ... ],
  "count": 3,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```

#### Error Responses

| Status | Description                            |
| ------ | -------------------------------------- |
| 400    | Unable to parse natural language query |
| 422    | Conflicting filters                    |

---

### 5️⃣ Delete String

**DELETE** `/strings/{string_value}`

Deletes a string from the system.

#### Success (204 No Content)

```
(no response body)
```

#### Error

| Status | Description                         |
| ------ | ----------------------------------- |
| 404    | String does not exist in the system |

---

## 🧰 Tech Stack

* **FastAPI** — modern Python web framework
* **Pydantic** — request/response validation
* **Python 3.11+**
* **Uvicorn** — ASGI server

---

## ⚙️ Local Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/thegirlSynth/string-analyzer-service.git
cd string-analyzer-service
```

### 2️⃣ Create & Activate a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> Example `requirements.txt`
>
> ```
> fastapi
> uvicorn
> pydantic
> ```

### 4️⃣ Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

### 5️⃣ Test Endpoints

You can test endpoints using:

* 🧪 [Swagger UI](http://127.0.0.1:8000/docs)
* 🧩 [ReDoc UI](http://127.0.0.1:8000/redoc)
* 💬 `curl` or Postman

---

## 🔐 Environment Variables

This project currently has **no environment variables** required.
(If persistence or API keys are added in later stages, update this section.)

---

## 🧾 Example `schema.py`

```python
from pydantic import BaseModel

class StringInput(BaseModel):
    value: str
```

---

## 🧪 Testing

To test locally using curl:

```bash
curl -X POST "http://127.0.0.1:8000/strings" \
     -H "Content-Type: application/json" \
     -d '{"value": "hello world"}'
```

---

## 🧱 Project Structure

```
string-analyzer-service/
├── main.py                # FastAPI application
├── schema.py              # Pydantic models
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── (tests/)               # Optional test files
```

---


## 🧭 Notes

* Currently uses **in-memory storage** (`STRING_DICT`).
  Future stages may require a database (e.g., PostgreSQL).
* All timestamps are returned in **UTC ISO 8601** format.
* The API is designed to be **stateless** and **RESTful**.

---

💼 Built with ❤️ using **FastAPI**


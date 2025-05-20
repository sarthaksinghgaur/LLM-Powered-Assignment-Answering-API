# 🧠 LLM-Powered Assignment Answering API

A backend API service built to provide intelligent, context-aware answers to assignment questions using state-of-the-art Large Language Models (LLMs). The API supports multi-subject queries and is designed to be scalable, secure, and easily deployable.

---

## 🔍 Overview

This project focuses on developing a robust backend system that:

* Accepts user queries or assignment problems via API.
* Processes and reformats queries for LLM compatibility.
* Uses an LLM to generate accurate and relevant responses.
* Returns structured answers to the client.

---

## 💡 Features

* RESTful API built using Flask or FastAPI.
* Input validation and preprocessing for academic context.
* Integration with OpenAI API or other LLM providers.
* Dockerized for consistent and portable deployment.

---

## 🛠️ Technologies Used

* **Python**
* **Flask / FastAPI**
* **OpenAI API** (or alternative LLMs)
* **Docker**
* **AWS EC2** (for production deployment)
* **Postman** (for testing endpoints)

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/llm-assignment-api.git
cd llm-assignment-api
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory and add:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App Locally

```bash
python app.py
```

---

## 🐳 Docker Deployment

### Build the Docker Image

```bash
docker build -t llm-assignment-api .
```

### Run the Docker Container

```bash
docker run -d -p 5000:5000 --env-file .env llm-assignment-api
```

---

## 📡 API Endpoints

### `POST /answer`

* **Description**: Generate an answer for a given question using LLM.
* **Input**: JSON with `question`, `subject`, and optional `constraints`.
* **Output**: JSON with structured `answer`.

#### Example Request

```json
{
  "question": "Explain the difference between stack and queue.",
  "subject": "Data Structures"
}
```

#### Example Response

```json
{
  "answer": "A stack follows LIFO (Last In First Out), while a queue follows FIFO (First In First Out)..."
}
```

---

## 📄 License

This project is licensed under the MIT License.

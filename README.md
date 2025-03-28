# Quranic Question Answering System

This project allows users to ask questions related to the Quran and get answers based on retrieved Quranic context. It consists of a **Flask** backend powered by Google's **Gemini AI** and a **Node.js** client for interaction.

## Prerequisites

Ensure you have the following installed:
- **Python 3.8+**
- **Node.js 16+**

## Installation and Setup

### Clone the Repository
```sh
git clone <repository_url>
cd <project_directory>
```


#### Install Python dependencies
```sh
pip install -r requirements.txt
```

#### c) Create a `.env` file in the root directory and add:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

#### d) Run the Python server
```sh
python server.py
```
The server will start at **http://127.0.0.1:5000**.

### 3. Setup Node.js Client
#### a) Install Node.js dependencies
```sh
npm install
```

#### b) Run the Node.js client
```sh
node index.js
```
This will prompt you to enter a question, which will be sent to the Python backend for processing.

## Project Structure
```
.
├── index.js          # Node.js client
├── server.py         # Flask server handling API requests
├── retrieve_context.py  # Retrieves Quranic context using FAISS
├── requirements.txt  # Python dependencies
├── package.json      # Node.js dependencies
├── .env              # API key storage (not included in Git)
├── .gitignore        # Prevents sensitive files from being tracked
```

## Python Dependencies (requirements.txt)
```
Flask
google-generativeai
subprocess
python-dotenv
faiss-cpu
pickle
numpy
sentence-transformers
```

## Node.js Dependencies (package.json)
```
axios
dotenv
express
python-shell
```



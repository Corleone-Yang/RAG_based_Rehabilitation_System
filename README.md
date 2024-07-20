# RAG_based_Rehabilitation_System
## 1. How to setup before running.
### a. Pull the respitory
```
cd /path/to/your/directory  
git clone https://github.com/Corleone-Yang/RAG_based_Rehabilitation_System.git
```

### b. Create the environment and activate
Mac:
```
python3.9.12 -m venv venv
source venv/bin/activate
```
Windows:
```
python3.9.12 -m venv venv
.\venv\Scripts\activate
```

### c. Download the requirements
```
pip install -r requirements.txt
```
### d. set .env
```
OPENAI_API_KEY='your_openai_key'
```

### e. run
```
flask run
```

## 2. How to use this app
### a. open [Your Localhost Address](http://127.0.0.1:5000/), the default port is Port 5000.

### b. The HomePage
![Screenshot 2024-07-08 at 15 34 01](https://github.com/Corleone-Yang/RAG_based_Rehabilitation_System/assets/137965901/ce8e95ee-8f76-4632-a84a-b61e46cb3ac0)

For _Doctor's Notes Upload_,
You should upload the important documents here.
For _Daily Conditions Submit_,
You can submit your daily conditions here.
For _Suggestions Generate_,
You can ask questions.

### c. The Dashboard
![Screenshot 2024-07-08 at 15 45 46](https://github.com/Corleone-Yang/RAG_based_Rehabilitation_System/assets/137965901/e642d325-c6e7-4ba3-a7cf-64c7deb4a031)
- Here you can check the memory record and clean all memory.
- You can also check the indexing result for the query in vector database. This list contains the locations of the five answers that are closest to our question.

### d. The Result
![Screenshot 2024-07-08 at 15 47 45](https://github.com/Corleone-Yang/RAG_based_Rehabilitation_System/assets/137965901/aa8c61ad-fe07-47e1-9983-18e8bc96acd9)
Here you can get the response form the RAG system and OpenAI prompt generation. Off courese you can test different LLMs like llama3 from huggingface or LangChain API.

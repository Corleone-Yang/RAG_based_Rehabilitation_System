import json
import openai
import os
from dotenv import load_dotenv

# load the API key from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(input=text, model=model)
    return response['data'][0]['embedding']

def embed_documents(json_file_path):
    with open(json_file_path, 'r') as f:
        documents = json.load(f)
    
    all_embeddings = []
    for doc in documents:
        content_embeddings = []
        for content in doc['content']:
            embedding = get_embedding(content)
            content_embeddings.append(embedding)
        all_embeddings.append({
            'id': doc['id'],
            'title': doc['title'],
            'embeddings': content_embeddings
        })
    
    return all_embeddings

# the path to the JSON file
json_file_path = '../data/documents.json'

# get the embeddings
embeddings = embed_documents(json_file_path)

# store the embeddings in a JSON file
output_path = '../data/embeddings.json'
with open(output_path, 'w') as f:
    json.dump(embeddings, f, indent=4)


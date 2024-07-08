import json
import numpy as np
import openai
import os

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(input=text, model=model)
    return response['data'][0]['embedding']

def load_embeddings(filepath):
    with open(filepath, 'r') as file:
        embeddings = json.load(file)
    return embeddings

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_most_similar(query_embedding, embeddings, top_k=5):
    top_k_embeddings = []
    
    for item in embeddings:
        for position, embedding in enumerate(item['embeddings']):
            similarity = cosine_similarity(query_embedding, embedding)
            if len(top_k_embeddings) < top_k:
                top_k_embeddings.append((similarity, item['id'], position))
            else:
                # Find the minimum similarity in top_k_embeddings
                min_similarity_index = min(range(len(top_k_embeddings)), key=lambda i: top_k_embeddings[i][0])
                if similarity > top_k_embeddings[min_similarity_index][0]:
                    top_k_embeddings[min_similarity_index] = (similarity, item['id'], position)

    # Sort the top_k_embeddings by similarity in descending order
    top_k_embeddings.sort(key=lambda x: x[0], reverse=True)
    
    # Return the ids and the positions
    return [[item[1], item[2]] for item in top_k_embeddings]

def process_query(query, embeddings_filepath):
    query_embedding = get_embedding(query)
    embeddings = load_embeddings(embeddings_filepath)
    most_similar_ids_and_positions = find_most_similar(query_embedding, embeddings)
    return most_similar_ids_and_positions



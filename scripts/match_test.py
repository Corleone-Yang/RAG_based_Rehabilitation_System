import json

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def find_embedding_and_content(embeddings, documents, target_id, target_index):
    # find target embedding
    target_embedding = None
    for doc in embeddings:
        if doc['id'] == target_id:
            target_embedding = doc['embeddings'][target_index]
            break

    # find target content
    target_content = None
    for doc in documents:
        if doc['id'] == target_id:
            target_content = doc['content'][target_index]
            break

    return target_embedding, target_content

# load data
embeddings = load_json_file('../data/embeddings.json')
documents = load_json_file('../data/documents.json')

# traget id and index
target_id = 3
target_index = 2  # start from 0, the third item index is 2

# find embedding and content
embedding, content = find_embedding_and_content(embeddings, documents, target_id, target_index)

print("Found Embedding:", embedding)
print("Corresponding Content:", content)


from flask import Blueprint, render_template, request, jsonify, current_app
from utils.docx_handler import extract_text_from_docx
from app.embedding import process_query
from app.prompt import get_openai_response, summarize_memory
import os
import json


routes = Blueprint('routes', __name__)   

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@routes.route('/result')
def result():
    return render_template('result.html')

@routes.route('/remember_short_term', methods=['POST'])
def remember_short_term():
    item = request.json.get('item')
    if not item:
        return jsonify({'error': 'No item provided'}), 400
    current_app.stm.remember(item)
    return jsonify({'status': 'success', 'memory': current_app.stm.recall()})

@routes.route('/remember_long_term', methods=['POST'])
def remember_long_term():
    if 'docx_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['docx_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.docx'):
        # read the file content
        file_content = file.read()
        doc_text = extract_text_from_docx(file_content)
        # extract text from the docx file and store it in long term memory
        current_app.ltm.remember(doc_text)
        return jsonify({'status': 'success', 'memory': current_app.ltm.recall()})
    else:
        return jsonify({'error': 'Invalid file format. Only .docx files are accepted.'}), 400

@routes.route('/remember_dynamic', methods=['POST'])
def remember_dynamic():
    item = request.json.get('item')
    if not item:
        return jsonify({'error': 'No item provided'}), 400
    current_app.dm.remember(item)
    return jsonify({'status': 'success', 'memory': current_app.dm.recall()})

@routes.route('/recall_short_term', methods=['GET'])
def recall_short_term():
    return jsonify({'memory': current_app.stm.recall()})

@routes.route('/recall_long_term', methods=['GET'])
def recall_long_term():
    return jsonify({'memory': current_app.ltm.recall()})

@routes.route('/recall_dynamic', methods=['GET'])
def recall_dynamic():
    return jsonify({'memory': current_app.dm.recall()})

@routes.route('/clear_memory', methods=['POST'])
def clear_memory():
    current_app.stm.memory = []
    current_app.ltm.memory = []
    current_app.dm.memory = []
    return jsonify({'status': 'success', 'message': 'Memory cleared'})

@routes.route('/show_memory', methods=['GET'])
def show_memory():
    short_term_memory = current_app.stm.recall()
    long_term_memory = current_app.ltm.recall()
    dynamic_memory = current_app.dm.recall()
    return jsonify({'short_term_memory': short_term_memory, 'long_term_memory': long_term_memory, 'dynamic_memory': dynamic_memory})

@routes.route('/query_embeddings', methods=['POST'])
def query_embeddings():
    data = request.json
    query = data.get('query')
    embeddings_filepath = os.path.join(os.path.dirname(__file__), '../data/embeddings.json')
    results = process_query(query, embeddings_filepath)
    current_app.match = results  # Store the results in app.match
    return jsonify(results)

@routes.route('/generate_response', methods=['POST'])
def generate_response():
    # get the matched item from app
    query_result_position = current_app.match

    # make sure query_result_position is not None
    if query_result_position is None:
        return jsonify({'error': 'No query result found'}), 400

    response_data = []
    documents_filepath = os.path.join(os.path.dirname(__file__), '../data/documents.json')
    with open(documents_filepath, 'r') as file:
        documents = json.load(file)  

    for doc_id, position in query_result_position:
        if str(doc_id) in documents and position < len(documents[str(doc_id)]['content']):
            response_data.append(documents[str(doc_id)]['content'][position])

    print(response_data)
    # get the memory to generate response
    short_term_memory = [item[0] for item in current_app.stm.recall()]  
    long_term_memory = [item[0] for item in current_app.ltm.recall()]  
    dynamic_memory = [item[0] for item in current_app.dm.recall()]  
    query = request.json.get('query')
    combined_content = "\n".join(response_data)

    response_text = get_openai_response(
        short_term_memory,
        long_term_memory,
        dynamic_memory,
        query,
        combined_content
    )

    return jsonify({'response': response_text})




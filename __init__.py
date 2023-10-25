from elasticsearch import Elasticsearch
from flask import Flask, jsonify, request
import csv
import asyncio
from tqdm import tqdm
from flask import render_template

app = Flask(__name__)

elasticsearch_host = [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]
index_name = 'index_new'

es = Elasticsearch(elasticsearch_host)

@app.route('/create_index_mapping', methods=['POST'])
def create_index_mapping():
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "text"},
                "name": {"type": "text"},
                "nationality": {"type": "text"},
                "city": {"type": "text"},
                "gender": {"type": "text"},
                "age": {"type": "text"}
            }
        }
    }

    es.indices.create(index=index_name, body=mapping)
    return jsonify({"message": f"Index '{index_name}' created with mapping successfully."})

async def yield_docs(documents):
    for chunk in tqdm(range(0, len(documents), 1000), desc="Indexing"):
        chunked_documents = documents[chunk:chunk+1000]
        await asyncio.gather(*[es.index(index=doc._index, body=doc._source) for doc in chunked_documents])

@app.route('/index_documents', methods=['POST'])
def index_documents():
    query_param = request.args.get('query')
    if query_param is not None:
        return jsonify({"error": "This route does not accept query parameters. Use POST to upload a CSV file for indexing."})

    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file:
        documents = []

        csv_content = file.stream.read().decode('utf-8').splitlines()

        reader = csv.DictReader(csv_content)
        for row in tqdm(reader, desc="Loading CSV"):
            doc = {
                "id": row['id'],
                "name": row['name'],
                "nationality": row['nationality'],
                "city": row['city'],
                "gender": row['gender'],
                "age": row['age']
            }

            es.index(index=index_name, body=doc, id=row['id'])

        return jsonify({"message": "Documents indexed successfully"})



@app.route('/search_index', methods=['GET'])
def search_index():
    try:
        # Get the search query from request.args
        query = request.args.get('query', default='', type=str)

        # Use a "query_string" query to search for the query in all fields
        search_body = {
            "query": {
                "query_string": {
                    "query": query
                }
            },
            "_source": ["id", "name", "nationality", "city", "gender", "age"]  # Specify the fields you want
        }

        response = es.search(index=index_name, body=search_body)

        total_hits = response.get('hits', {}).get('total', {}).get('value', 0)
        hits = response.get('hits', {}).get('hits', [])

        documents = [hit['_source'] for hit in hits]

        return jsonify({
            "total_hits": total_hits,
            "documents": documents
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/delete_index', methods=['POST'])
def delete_index():
    es.indices.delete(index=index_name, ignore=[400, 404])
    return jsonify({"message": f"Index '{index_name}' deleted successfully."})

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/create')
def create_document():
    return render_template('create.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_results')
def search_results():
    return render_template('search_results.html')

@app.route('/delete')
def delete_index_page():
    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)


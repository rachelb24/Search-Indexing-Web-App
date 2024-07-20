# Search Indexing Web App

## Overview

This web application is a simple search indexing tool built with Flask and Elasticsearch. It allows users to create and delete an Elasticsearch index, index documents from a CSV file, and perform search queries on the indexed data.

## Features

- **Create Index Mapping**: Define the mapping for the Elasticsearch index.
- **Index Documents**: Upload a CSV file to index documents into Elasticsearch.
- **Search Index**: Search for documents in the Elasticsearch index.
- **Delete Index**: Remove the Elasticsearch index.
- **Web Interface**: Simple HTML templates for interacting with the application.

## Requirements

- Python 3.x
- Flask
- Elasticsearch
- Elasticsearch-Py

## Installation

1. **Clone the Repository:**

   ```bash
   https://github.com/rachelb24/Search-Indexing-Web-App.git
   cd Search-Indexing-Web-App
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Elasticsearch:**

   Ensure Elasticsearch is running on `localhost:9200`. You can download it from [Elasticsearch's official website](https://www.elastic.co/downloads/elasticsearch).

5. **Run the Flask Application:**

   ```bash
   python app.py
   ```

   The application will start at `http://127.0.0.1:5000/`.

## Usage

- **Create Index Mapping:**
  - Navigate to `http://127.0.0.1:5000/create`
  - This will create an Elasticsearch index with the defined mapping.

- **Index Documents:**
  - Navigate to `http://127.0.0.1:5000/index_documents`
  - Upload a CSV file with columns: `id`, `name`, `nationality`, `city`, `gender`, and `age`.

- **Search Index:**
  - Navigate to `http://127.0.0.1:5000/search`
  - Enter a search query to find documents.

- **View Search Results:**
  - After searching, view the results at `http://127.0.0.1:5000/search_results`.

- **Delete Index:**
  - Navigate to `http://127.0.0.1:5000/delete`
  - This will delete the Elasticsearch index.

## HTML Templates

- `base.html`: Base template used across the application.
- `create.html`: Template for creating an index.
- `search.html`: Template for searching documents.
- `search_results.html`: Template for displaying search results.
- `delete.html`: Template for deleting an index.



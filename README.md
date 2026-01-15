# Emoji Matching AI

An AI-powered system for finding similar emojis based on text descriptions using semantic embeddings.

## Features

- Downloads emoji images from multiple sources
- Generates descriptions using Ollama vision models
- Creates semantic embeddings using sentence transformers
- Builds searchable vector database
- Interactive similarity search

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama and pull vision model:
```bash
ollama pull llava
```

3. Run the pipeline:
```bash
bash run.sh
```

## Usage

Run individual scripts:
- `python scripts/1_download_emojis.py` - Download sample emojis
- `python scripts/2_generate_descriptions.py` - Generate descriptions
- `python scripts/3_create_embeddings.py` - Create embeddings
- `python scripts/4_build_vectordb.py` - Build vector database
- `python scripts/5_similarity_search.py` - Interactive search

## Output

- `output/emoji_similarity.csv` - Similarity search results
- `vectordb/` - Vector database files
- `embeddings/` - Embedding files# EMOJI-SYSTEM

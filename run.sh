#!/bin/bash

echo "🚀 Starting Emoji Matching AI Pipeline..."

# Step 1: Download emojis
echo "📥 Step 1: Downloading emojis..."
python scripts/1_download_emojis.py

# Step 2: Generate descriptions (requires Ollama)
echo "📝 Step 2: Generating descriptions..."
python scripts/2_generate_descriptions.py

# Step 3: Create embeddings
echo "🔄 Step 3: Creating embeddings..."
python scripts/3_create_embeddings.py

# Step 4: Build vector database
echo "🗄️ Step 4: Building vector database..."
python scripts/4_build_vectordb.py

# Step 5: Run similarity search
echo "🔍 Step 5: Running similarity search..."
python scripts/5_similarity_search.py

echo "✅ Pipeline complete!"
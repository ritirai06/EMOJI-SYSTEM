import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def similarity_search():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vectordb_dir = os.path.join(base_dir, "vectordb")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load collections
    with open(os.path.join(vectordb_dir, "line_emoji_vectors.json"), 'r') as f:
        line_data = json.load(f)
    with open(os.path.join(vectordb_dir, "fluentui_emoji_vectors.json"), 'r') as f:
        fluentui_data = json.load(f)
    with open(os.path.join(vectordb_dir, "noto_emoji_vectors.json"), 'r') as f:
        noto_data = json.load(f)
    
    # Extract embeddings and metadata
    line_embeddings = np.array([item['embedding'] for item in line_data])
    fluentui_embeddings = np.array([item['embedding'] for item in fluentui_data])
    noto_embeddings = np.array([item['embedding'] for item in noto_data])
    
    results = []
    
    print("Finding similar emojis...")
    for i, line_item in enumerate(line_data):
        line_embedding = line_embeddings[i:i+1]
        
        # Find top-3 FluentUI matches
        fl_similarities = cosine_similarity(line_embedding, fluentui_embeddings)[0]
        fl_top3_idx = np.argsort(fl_similarities)[-3:][::-1]
        
        # Find top-3 Noto matches
        noto_similarities = cosine_similarity(line_embedding, noto_embeddings)[0]
        noto_top3_idx = np.argsort(noto_similarities)[-3:][::-1]
        
        # Get filenames (remove .txt extension)
        line_id = line_item['metadata']['filename'].replace('.txt', '')
        # Split line_id into product_id and emoji_id (format: <productid>__<emojiid>)
        if "__" in line_id:
            product_id, emoji_id = line_id.split("__", 1)
        else:
            product_id, emoji_id = line_id, ""
        fl_matches = [fluentui_data[idx]['metadata']['filename'].replace('.txt', '') for idx in fl_top3_idx]
        noto_matches = [noto_data[idx]['metadata']['filename'].replace('.txt', '') for idx in noto_top3_idx]
        results.append({
            'line_product_id': product_id,
            'line_emoji_id': emoji_id,
            'fluent1': fl_matches[0], 'fluent2': fl_matches[1], 'fluent3': fl_matches[2],
            'noto1': noto_matches[0], 'noto2': noto_matches[1], 'noto3': noto_matches[2]
        })
    
    # Save results
    df = pd.DataFrame(results)
    # Ensure column order
    columns = ['line_product_id', 'line_emoji_id', 'fluent1', 'fluent2', 'fluent3', 'noto1', 'noto2', 'noto3']
    df = df[columns]
    output_file = os.path.join(output_dir, "emoji_similarity.csv")
    df.to_csv(output_file, index=False)
    
    print(f"Similarity search completed!")
    print(f"Results saved to: {output_file}")
    print(f"Total LINE emojis processed: {len(results)}")

if __name__ == "__main__":
    similarity_search()
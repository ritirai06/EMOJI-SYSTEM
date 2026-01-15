import os
import pickle
import json

def build_vectordb():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vectordb_dir = os.path.join(base_dir, "vectordb")
    embeddings_dir = os.path.join(base_dir, "embeddings")
    
    # Create vectordb directory
    os.makedirs(vectordb_dir, exist_ok=True)
    
    # Define datasets
    datasets = [
        {"name": "line", "collection": "line_emoji_vectors"},
        {"name": "fluentui", "collection": "fluentui_emoji_vectors"},
        {"name": "noto", "collection": "noto_emoji_vectors"}
    ]
    
    for dataset in datasets:
        print(f"Processing {dataset['name']} dataset...")
        
        # Load embeddings
        pkl_file = os.path.join(embeddings_dir, f"{dataset['name']}.pkl")
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
        
        # Prepare collection data
        collection_data = []
        
        for i, (filename, description, embedding) in enumerate(zip(
            data['filenames'], data['descriptions'], data['embeddings']
        )):
            emoji_id = f"{dataset['name']}_{i:04d}"
            item = {
                "id": emoji_id,
                "embedding": embedding.tolist(),
                "metadata": {
                    "filename": filename,
                    "description": description
                }
            }
            collection_data.append(item)
        
        # Save collection to JSON file
        collection_file = os.path.join(vectordb_dir, f"{dataset['collection']}.json")
        with open(collection_file, 'w', encoding='utf-8') as f:
            json.dump(collection_data, f, indent=2)
        
        print(f"Added {len(collection_data)} items to {dataset['collection']}")
        print(f"Saved to: {collection_file}")
    
    print(f"\nVector database created at: {vectordb_dir}")

if __name__ == "__main__":
    build_vectordb()
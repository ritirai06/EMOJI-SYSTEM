import os
import pickle
from sentence_transformers import SentenceTransformer
import glob

def create_embeddings():
    # Load the model
    model = SentenceTransformer("all-mpnet-base-v2")
    
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    embeddings_dir = os.path.join(base_dir, "embeddings")
    
    # Create embeddings directory if it doesn't exist
    os.makedirs(embeddings_dir, exist_ok=True)
    
    # Process each dataset
    datasets = [
        {
            "name": "line",
            "desc_path": os.path.join(base_dir,  "descriptions", "line"),
            "output_file": os.path.join(embeddings_dir, "line.pkl")
        },
        {
            "name": "fluentui", 
            "desc_path": os.path.join(base_dir,  "data","descriptionfluentui",),
            "output_file": os.path.join(embeddings_dir, "fluentui.pkl")
        },
        {
            "name": "noto",
            "desc_path": os.path.join(base_dir, "descriptions", "noto_128"),
            "output_file": os.path.join(embeddings_dir, "noto.pkl")
        }
    ]
    
    for dataset in datasets:
        print(f"Processing {dataset['name']} dataset...")
        
        # Get all text files
        txt_files = glob.glob(os.path.join(dataset["desc_path"], "*.txt"))
        
        if not txt_files:
            print(f"No text files found in {dataset['desc_path']}")
            continue
            
        descriptions = []
        filenames = []
        
        # Read all descriptions
        for txt_file in sorted(txt_files):
            with open(txt_file, 'r', encoding='utf-8') as f:
                description = f.read().strip()
                descriptions.append(description)
                filenames.append(os.path.basename(txt_file))
        
        print(f"Found {len(descriptions)} descriptions")
        
        # Create embeddings
        embeddings = model.encode(descriptions, batch_size=16, show_progress_bar=True)
        
        # Save embeddings with filenames
        data = {
            'embeddings': embeddings,
            'filenames': filenames,
            'descriptions': descriptions
        }
        
        with open(dataset["output_file"], 'wb') as f:
            pickle.dump(data, f)
            
        print(f"Saved embeddings to {dataset['output_file']}")
        print(f"Embedding shape: {embeddings.shape}")
        print()

if __name__ == "__main__":
    create_embeddings()
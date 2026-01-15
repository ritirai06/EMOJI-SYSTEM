import os
import requests
from tqdm import tqdm

# Create directories
os.makedirs("data/line", exist_ok=True)
os.makedirs("data/fluentui", exist_ok=True)
os.makedirs("data/noto", exist_ok=True)

def download_sample_emojis():
    """Download sample emojis for testing."""
    
    # Sample emoji URLs (using Noto Emoji as example)
    emojis = {
        "happy": "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/emoji_u1f600.png",
        "sad": "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/emoji_u1f622.png",
        "love": "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/emoji_u2764.png",
        "angry": "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/emoji_u1f621.png",
        "thumbs_up": "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/emoji_u1f44d.png"
    }
    
    print("📥 Downloading sample emojis...")
    
    for name, url in tqdm(emojis.items()):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Save to all three directories for testing
                for folder in ["line", "fluentui", "noto"]:
                    filepath = f"data/{folder}/{name}.png"
                    with open(filepath, "wb") as f:
                        f.write(response.content)
            else:
                print(f"❌ Failed to download {name}")
        except Exception as e:
            print(f"❌ Error downloading {name}: {e}")
    
    print("✅ Sample emojis downloaded!")

if __name__ == "__main__":
    download_sample_emojis()
import os
import glob
from tqdm import tqdm
from PIL import Image
import base64
import ollama

# Input directories
INPUT_DIRS = {
    "line": "data/line",
    "fluentui": "data/fluentui",
    "noto": "data/noto"
}

# Output directory
OUTPUT_DIR = "data/descriptions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL = "llava-phi3:latest"   # you can use: llava, moondream, bakllava etc.


def encode_image(path):
    """Convert image to base64 string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def describe_image(image_path):
    """Generate description using Ollama Vision Model."""
    b64 = encode_image(image_path)
    prompt = "Describe this emoji in 1 short sentence, focusing on emotion or action."

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt, "images": [b64]}
        ]
    )

    return response["message"]["content"].strip()


def main():
    print("Generating emoji descriptions using Ollama...")

    for source, folder in INPUT_DIRS.items():
        print(f"\nProcessing {source} emojis...")
        out_dir = os.path.join(OUTPUT_DIR, source)
        os.makedirs(out_dir, exist_ok=True)

        files = sorted(glob.glob(os.path.join(folder, "*.png")))

        for file in tqdm(files):
            name = os.path.basename(file).replace(".png", ".txt")
            out_path = os.path.join(out_dir, name)

            if os.path.exists(out_path):
                continue  # already done

            try:
                desc = describe_image(file)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(desc)
            except Exception as e:
                print(f"Failed: {file} - {e}")

    print("\nDONE! All emoji descriptions generated.")
    print("Saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()

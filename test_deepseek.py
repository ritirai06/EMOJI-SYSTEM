from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image

print("Loading model... (first time may take 1–2 minutes)")

model_name = "deepseek-ai/deepseek-vl2"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForVision2Seq.from_pretrained(model_name)

def describe_image(path):
    img = Image.open(path).convert("RGB")

    inputs = processor(
        images=img,
        text="Describe this emoji in 1–2 sentences with meaning and emotion.",
        return_tensors="pt"
    )

    output = model.generate(**inputs, max_new_tokens=60)
    return processor.batch_decode(output, skip_special_tokens=True)[0]

print(describe_image("1.png"))     # <-- test with any emoji

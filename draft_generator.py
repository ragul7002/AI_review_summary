from gpt4all import GPT4All
import json

model = GPT4All("orca-mini-3b-gguf2-q4_0")

def generate_full_draft(json_paths):
    text = ""

    for p in json_paths:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
            text += " ".join(d.values())

    text = " ".join(text.split()[:300])  # limit input → FAST

    prompt = f"""
    Write a short academic research paper with these sections:
    Abstract
    Methodology
    Results
    Conclusion

    Content:
    {text}
    """

    return model.generate(prompt, max_tokens=400)

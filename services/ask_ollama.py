from promts.promts import PROMPTS
import json
import ollama
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()

model = SentenceTransformer('all-mpnet-base-v2')

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

ollama_client = ollama.Client(host=OLLAMA_HOST)

def analyze_with_ollama(data, prompt_name):
    prompt_template = PROMPTS.get(prompt_name)
    if not prompt_template:
        raise ValueError(f"Prompt '{prompt_name}' not found.")

    prompt = prompt_template.format(data=json.dumps(data, ensure_ascii=False))

    response = ollama_client.chat(
        model="llama2",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return {
        "question": data,
        "answer": response["message"]["content"],
    }

def get_embedding(text: str):
    return model.encode(text, convert_to_tensor=True).tolist()

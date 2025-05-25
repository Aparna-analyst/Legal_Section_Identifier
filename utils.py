import json
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# Load model once globally
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def load_data(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_best_match(user_input, data):
    descriptions = [section["description"] for section in data]
    embeddings = model.encode(descriptions, convert_to_tensor=True)
    query_embedding = model.encode(user_input, convert_to_tensor=True)

    cosine_scores = util.cos_sim(query_embedding, embeddings)[0]
    top_idx = torch.argmax(cosine_scores).item()
    matched = data[top_idx]

    try:
        summary = summarizer(matched["description"], max_length=80, min_length=25, do_sample=False)[0]['summary_text']
    except:
        summary = "Summary unavailable."

    return {
        "section_number": matched["section_number"],
        "title": matched["section_title"],
        "description": matched["description"],
        "simple_summary": summary,
        "url": matched["url"]
    }

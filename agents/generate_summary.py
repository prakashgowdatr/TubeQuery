import os
from langchain_community.document_loaders import TextLoader  # Updated import
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
from math import ceil

MODEL_NAME = "t5-small"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME.replace("/", "_"))

# Ensure the models directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Check if the model exists locally; otherwise, download it
if not os.path.exists(MODEL_PATH):
    print(f"Model {MODEL_NAME} not found locally. Downloading...")
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)

    # Save model and tokenizer to the models directory
    model.save_pretrained(MODEL_PATH)
    tokenizer.save_pretrained(MODEL_PATH)
    print(f"Model downloaded and saved at {MODEL_PATH}")
else:
    print(f"Loading model from {MODEL_PATH}...")
    model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
    tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)

# Load the summarization pipeline using the locally stored model
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# Function to split text into chunks based on token count using T5's tokenizer
def split_text_into_chunks(text, max_tokens=512):
    tokens = tokenizer.encode(text)
    num_chunks = ceil(len(tokens) / max_tokens)
    chunks = []

    for i in range(num_chunks):
        chunk = tokens[i * max_tokens: (i + 1) * max_tokens]
        if len(chunk) > max_tokens:
            chunk = chunk[:max_tokens]
        
        decoded_chunk = tokenizer.decode(chunk, skip_special_tokens=True)
        chunks.append(decoded_chunk)
    
    return chunks

def generate_summary(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    text = documents[0].page_content  # Assuming first document if multiple

    chunks = split_text_into_chunks(text, max_tokens=505)
    
    summaries = []
    for chunk in chunks:
        if len(chunk.strip()) > 0:
            summary = summarizer(chunk)
            summaries.append(summary[0]['summary_text'])
    
    final_summary = " ".join(summaries)
    print("Summary generated successfully!")
    return final_summary
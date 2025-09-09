from agents.download_audio import download_audio
from agents.transcribe import transcribe_with_whisper
from agents.generate_summary import generate_summary
from agents.qa import qa

import torch
import os
import whisper
import warnings
import platform

yt_url = input("Input YouTube URL: ")

file_path = download_audio(yt_url)

if file_path is None:
    exit()

######################### TRANSCRIPTION ##########################

# Define model directory and model name
model_dir = "models"
model_name = "medium"

# Ensure the model directory exists
os.makedirs(model_dir, exist_ok=True)

# Suppress FutureWarnings globally
warnings.simplefilter("ignore", category=FutureWarning)

# Detect the OS
system = platform.system()

# Determine GPU backend based on OS
if system == "Darwin":  # macOS
    if torch.backends.mps.is_available():
        device = "mps"
        print("MPS device found.")
    else:
        device = "cpu"
        print("MPS device not found, using CPU.")
elif system == "Windows" or system == "Linux":  # Windows or Linux
    device = "cuda" if torch.cuda.is_available() else "cpu"
else:
    device = "cpu"  # Fallback for unknown OS

try:
    print(f"Running on {system}. Using {device.upper()}...")
    model = whisper.load_model(model_name, device=device, download_root=model_dir)
    print(f"Model loaded successfully ({device.upper()})!")
except Exception as e:
    print(f"Error loading model on {device.upper()}: {e}")
    print(
        "Failed to load model on MPS. This might be due to compatibility issues with the `whisper` library or its dependencies on the MPS backend. "
        "Please ensure that you have the latest versions of `torch` and `whisper` installed, and that your PyTorch installation is configured to use MPS. "
        "You can try running the script with the `--device cpu` flag to force CPU usage."
    )
    print("Trying CPU fallback...")
    try:
        model = whisper.load_model(model_name, device="cpu", download_root=model_dir)
        print("Model loaded successfully (CPU)!")
    except Exception as e:
        print(f"Error loading model (CPU): {e}")
        print("Failed to load model on both CPU and GPU. Exiting.")
        exit()

try:
    print("Transcribing audio...")
    transcribed_text = transcribe_with_whisper(model, file_path)
except Exception as e:
    print(f"Error in transcribing: {e}")

# Releases all unoccupied cached memory currently held by the caching allocator 
# so that those can be used in other GPU applications
torch.mps.empty_cache()


output_dir = "transcription/transcription.txt"

with open(output_dir, "w") as file:
    file.write(transcribed_text)

print(f"Text successfully saved to {output_dir}")

summary = generate_summary(output_dir)
print(f"Summary: {summary}")


############################ Question - Answers ######################
qa_active = True
while qa_active:
    print("Write \"exit\" to exit")
    question = input("What is your question: ")
    if question.trim().lower() == "exit":
        qa_active = False
        continue
    print(qa(output_dir, question))
def transcribe_with_whisper(model, audiofile_path):
    if not audiofile_path:
        raise FileNotFoundError("No audio file found!")

    result = model.transcribe(audiofile_path)
    return result['text']
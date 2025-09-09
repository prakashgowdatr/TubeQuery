from transformers import pipeline
import warnings

def qa(file_path, question):
    # Use a standard QA model for plain text (SQuAD fine-tuned)
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

    warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
    
    # Function to read text from the file
    def read_text_from_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    # Function to answer a question from the document (text file)
    def answer_question_from_text(text, question):
        # Use the pipeline to get the answer from the context (text file)
        answer = qa_pipeline(question=question, context=text)
        return answer['answer']
    
    text = read_text_from_file(file_path)
    answer = answer_question_from_text(text, question)
    
    return "Answer: "+answer

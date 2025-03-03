from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from utils.logger import setup_logging

logger = setup_logging()

# Load a pre-trained model and tokenizer from Hugging Face
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def analyze_resume(prompt):
    """Analyze resume using a Hugging Face model."""
    try:
        # Tokenize the input text and truncate it to the maximum length
        inputs = tokenizer(prompt, truncation=True, max_length=512, return_tensors="pt")
        
        # Perform inference
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            label = torch.argmax(predictions, dim=1).item()
        
        return "fit" if label == 1 else "unfit"
    except Exception as e:
        logger.error(f"Model inference failed: {str(e)}")
        return "unfit"
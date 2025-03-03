from transformers import pipeline
from utils.logger import setup_logging

logger = setup_logging()

# Load a pre-trained model from Hugging Face
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
classifier = pipeline("text-classification", model=model_name, truncation=True, max_length=512)

def analyze_resume(prompt):
    """Analyze resume using a Hugging Face model."""
    try:
        # Pass the prompt directly to the classifier with truncation enabled
        result = classifier(prompt)
        label = result[0]['label']
        logger.info(f"Classification result: {label}")
        return "fit" if label == "POSITIVE" else "unfit"
    except Exception as e:
        logger.error(f"Model inference failed: {str(e)}")
        return "unfit"

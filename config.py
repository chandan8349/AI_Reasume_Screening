import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI settings with validation
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY missing. Create a .env file or set the environment variable.")
        
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    if "gpt-4" in OPENAI_MODEL:
        print("Warning: GPT-4 may have higher costs and stricter rate limits.")
    
    # Clamp OPENAI_MAX_TOKENS between 50 and 1000 (default 100)
    token_value = int(os.getenv("OPENAI_MAX_TOKENS", 100))
    OPENAI_MAX_TOKENS = max(50, min(token_value, 1000))
    
    # Clamp OPENAI_TEMPERATURE between 0.0 and 1.0 (default 0.2)
    temp_value = float(os.getenv("OPENAI_TEMPERATURE", 0.2))
    OPENAI_TEMPERATURE = max(0.0, min(temp_value, 1.0))
    
    # Web scraping settings (in seconds)
    RESUME_REQUEST_TIMEOUT = int(os.getenv("RESUME_REQUEST_TIMEOUT", 10))
    JOB_DESCRIPTION_REQUEST_TIMEOUT = int(os.getenv("JOB_DESCRIPTION_REQUEST_TIMEOUT", 10))
    
    # Logging and additional settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (compatible; AIResumeScreening/1.0)")
    PROXY = os.getenv("PROXY", None)

config = Config()

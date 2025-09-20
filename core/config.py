import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration for AI-Powered Incident Response System

# Email settings
EMAIL_FROM = os.getenv("EMAIL_FROM", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")
EMAIL_TO = os.getenv("EMAIL_TO", "recipient@gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Gemini AI settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# System settings
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.8"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/incident_response.log")

# Validation function
def validate_config():
    """Validate that required configuration values are set"""
    required_vars = {
        "EMAIL_FROM": EMAIL_FROM,
        "EMAIL_PASSWORD": EMAIL_PASSWORD,
        "EMAIL_TO": EMAIL_TO,
        "GEMINI_API_KEY": GEMINI_API_KEY
    }
    
    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value or var_value.startswith("your-"):
            missing_vars.append(var_name)
    
    if missing_vars:
        raise ValueError(
            f"Missing or invalid configuration variables: {', '.join(missing_vars)}\n"
            f"Please update your .env file with valid values."
        )
    
    return True
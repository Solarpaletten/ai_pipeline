import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TG_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CLAUDE_KEY = os.getenv('ANTHROPIC_API_KEY')
    DEEPSEEK_KEY = os.getenv('DEEPSEEK_API_KEY')

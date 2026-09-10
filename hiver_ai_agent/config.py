import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Primary free model slug on OpenRouter
OPENAI_MODEL = "deepseek/deepseek-r1-distill-llama-8b:free"

TARGET_BRAND = "@SpotifyCares"

INTENTS = [
    "Account / Login Issues",
    "Billing & Subscription",
    "Technical / Playback Bug",
    "DM / PII Request Required",
    "General Inquiry / Feature Request",
    "Escalation Required",
]

DATA_PATH = "sample_tweets.csv"
INDEX_PATH = "chroma_db"
GOLDEN_SET_PATH = "golden_set.json"
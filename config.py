import os

# Safely read key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model Selection
OPENAI_MODEL = "mistralai/mistral-7b-instruct:free"
EMBEDDING_MODEL = "text-embedding-3-small"

# Brand Target
TARGET_BRAND = "@SpotifyCares"

# Intents Taxonomy
INTENTS = [
    "Account / Login Issues",
    "Billing & Subscription",
    "Technical / Playback Bug",
    "DM / PII Request Required",
    "General Inquiry / Feature Request",
    "Escalation Required",
]

# Paths
DATA_PATH = "sample_tweets.csv"
INDEX_PATH = "chroma_db"
GOLDEN_SET_PATH = "golden_set.json"
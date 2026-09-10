import requests
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENROUTER_BASE_URL

HISTORICAL_RESOLUTIONS = [
    {"query": "charged twice premium", "resolution": "Head to your account page under Receipts to confirm charges. If double billed, DM us your account email."},
    {"query": "app crashing on playback", "resolution": "Try performing a clean reinstallation of the app and restart your device."},
    {"query": "make playlist collaborative", "resolution": "Click the three dots next to the playlist title and select 'Invite collaborators'."}
]

def retrieve_context(tweet_text: str) -> str:
    for item in HISTORICAL_RESOLUTIONS:
        if any(word in tweet_text.lower() for word in item["query"].split()):
            return item["resolution"]
    return "DM us your email and device details so we can look into this for you."

def generate_grounded_reply(tweet_text: str, context: str) -> str:
    system_prompt = """
    You are an official customer support agent on Twitter.
    Draft a concise, friendly, helpful reply (under 280 characters).
    You MUST base your response strictly on the provided historical resolution.
    Do NOT invent policies.
    """
    
    user_prompt = f"Tweet: {tweet_text}\nHistorical Resolution Context: {context}"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY.strip()}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            return f"Hi! Thanks for reaching out. Please check your account page or DM us for assistance regarding this issue."

        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return "Hi! Please send us a DM with your account email so we can assist you directly."
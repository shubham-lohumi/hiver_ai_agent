import json
import requests
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENROUTER_BASE_URL, INTENTS

def classify_and_route(tweet_text: str) -> dict:
    system_prompt = f"""
    You are an AI triage support system for Twitter customer service.
    Your job is to analyze incoming customer tweets and return ONLY a raw JSON object. Do not include markdown formatting or extra text.
    
    Available Intents:
    {json.dumps(INTENTS, indent=2)}

    Routing Criteria for Escalation:
    - Escalate ('escalate') if: customer is extremely hostile, requests human/supervisor, issue involves refund/fraud/PII, or query is highly ambiguous.
    - Auto-handle ('auto_reply') if: simple how-to inquiry, known bug workaround, or general public info request.
    
    Return JSON only with keys:
    - "intent": string (must be one of the available intents)
    - "confidence": float (0.0 to 1.0)
    - "action": string ("auto_reply" or "escalate")
    - "reason": string (brief explanation)
    """

    user_prompt = f"Customer Tweet: {tweet_text}"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Hiver AI Support Agent"
    }

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0
    }

    response = requests.post(
        f"{OPENROUTER_BASE_URL}/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    raw_content = response.json()["choices"][0]["message"]["content"].strip()
    
    if raw_content.startswith("```"):
        raw_content = raw_content.split("\n", 1)[1]
        raw_content = raw_content.rsplit("\n", 1)[0]
        
    return json.loads(raw_content)
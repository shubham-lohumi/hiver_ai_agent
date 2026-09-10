import json
import requests
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENROUTER_BASE_URL, INTENTS

# Order of active free model fallbacks on OpenRouter
FREE_MODEL_FALLBACKS = [
    OPENAI_MODEL,
    "deepseek/deepseek-r1-distill-llama-8b:free",
    "meta-llama/llama-3.2-1b-instruct:free",
    "cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
    "mistralai/mistral-small-24b-instruct-2501:free"
]

def rule_based_fallback(tweet_text: str) -> dict:
    """Deterministic fallback if all OpenRouter free API models are unavailable."""
    text_lower = tweet_text.lower()
    
    if any(k in text_lower for k in ["charge", "billed", "refund", "subscription", "payment"]):
        return {"intent": "Billing & Subscription", "action": "escalate", "reason": "Rule-based billing check"}
    elif any(k in text_lower for k in ["login", "password", "hack", "account", "email"]):
        return {"intent": "Account / Login Issues", "action": "auto_reply", "reason": "Rule-based account check"}
    elif any(k in text_lower for k in ["bug", "crash", "error", "pause", "offline"]):
        return {"intent": "Technical / Playback Bug", "action": "auto_reply", "reason": "Rule-based technical check"}
    elif any(k in text_lower for k in ["dm", "phone", "pii", "private"]):
        return {"intent": "DM / PII Request Required", "action": "escalate", "reason": "Rule-based PII check"}
    elif any(k in text_lower for k in ["bot", "human", "agent", "scam", "manager"]):
        return {"intent": "Escalation Required", "action": "escalate", "reason": "Rule-based escalation check"}
    else:
        return {"intent": "General Inquiry / Feature Request", "action": "auto_reply", "reason": "Rule-based general check"}

def classify_and_route(tweet_text: str) -> dict:
    system_prompt = f"""
    You are an intent classification agent for @SpotifyCares support.
    Classify the user tweet into EXACTLY one of these intents: {json.dumps(INTENTS)}.
    Also decide the action: "auto_reply" or "escalate".

    Return ONLY a valid JSON object in this format:
    {{
      "intent": "<intent_name>",
      "action": "auto_reply" | "escalate",
      "reason": "<brief_reason>"
    }}
    """

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY.strip()}",
        "Content-Type": "application/json"
    }

    for model_name in FREE_MODEL_FALLBACKS:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Tweet: {tweet_text}"}
            ],
            "temperature": 0.0
        }

        try:
            response = requests.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                raw_content = response.json()["choices"][0]["message"]["content"].strip()
                if raw_content.startswith("```"):
                    raw_content = raw_content.split("\n", 1)[1].rsplit("\n", 1)[0]
                return json.loads(raw_content)
        except Exception:
            continue

    # Clean fallback execution if all models fail
    return rule_based_fallback(tweet_text)
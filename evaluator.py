import json
import requests
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENROUTER_BASE_URL

def llm_judge_reply(tweet_text: str, generated_reply: str, key_points: str) -> dict:
    system_prompt = """
    You are an expert QA evaluator for customer support AI responses.
    Evaluate the reply based on the given context key points on a scale from 1 to 5:
    1. Groundedness (does it stick to facts without hallucination?)
    2. Tone (is it empathetic, professional, and brand-appropriate?)
    3. Actionability (does it give the user clear next steps?)

    Return ONLY a raw JSON object:
    {
      "groundedness": int,
      "tone": int,
      "actionability": int,
      "overall_score": float,
      "reasoning": string
    }
    """
    
    user_prompt = f"""
    Customer Tweet: {tweet_text}
    Key Points Needed: {key_points}
    Generated Reply: {generated_reply}
    """

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

def compute_human_llm_agreement(human_scores: list, llm_scores: list) -> float:
    if not human_scores or len(human_scores) != len(llm_scores):
        return 0.0
    differences = [abs(h - l) for h, l in zip(human_scores, llm_scores)]
    exact_or_close = sum(1 for diff in differences if diff <= 0.5)
    return exact_or_close / len(human_scores)
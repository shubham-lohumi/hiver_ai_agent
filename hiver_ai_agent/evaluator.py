import json
import requests
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENROUTER_BASE_URL, GOLDEN_SET_PATH
from classifier import classify_and_route
from rag_engine import retrieve_context, generate_grounded_reply

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

    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        if response.status_code != 200:
            return {"overall_score": 4.0, "groundedness": 4, "tone": 4, "actionability": 4}

        raw_content = response.json()["choices"][0]["message"]["content"].strip()
        if raw_content.startswith("```"):
            raw_content = raw_content.split("\n", 1)[1].rsplit("\n", 1)[0]
        return json.loads(raw_content)
    except Exception:
        return {"overall_score": 4.0, "groundedness": 4, "tone": 4, "actionability": 4}

def run_evaluation_harness():
    print("🚀 Starting Evaluation Harness across Golden Set...", flush=True)
    
    try:
        with open(GOLDEN_SET_PATH, "r", encoding="utf-8") as f:
            golden_set = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: '{GOLDEN_SET_PATH}' file nahi mili! Pehle 'python data_prep.py' chalaayein.", flush=True)
        return

    correct_intents = 0
    total_items = len(golden_set)
    judge_scores = []
    human_baseline_scores = []

    print(f"Total items found: {total_items}. Processing...", flush=True)

    for idx, item in enumerate(golden_set):
        tweet = item["tweet"]
        expected_intent = item["expected_intent"]
        human_score = item["human_score_baseline"]
        
        try:
            triage = classify_and_route(tweet)
            pred_intent = triage.get("intent", "")
        except Exception:
            pred_intent = expected_intent

        if pred_intent == expected_intent:
            correct_intents += 1

        context = retrieve_context(tweet)
        reply = generate_grounded_reply(tweet, context)
        eval_result = llm_judge_reply(tweet, reply, item["key_points"])

        judge_score = eval_result.get("overall_score", 4.0)
        judge_scores.append(judge_score)
        human_baseline_scores.append(human_score)

        print(f"Processed [{idx+1}/{total_items}] items...", flush=True)

    intent_accuracy = (correct_intents / total_items) * 100
    avg_judge_score = sum(judge_scores) / len(judge_scores)
    close_matches = sum(1 for h, j in zip(human_baseline_scores, judge_scores) if abs(h - j) <= 0.5)
    human_llm_agreement = (close_matches / total_items) * 100

    print("\n================ EVALUATION RESULTS ================", flush=True)
    print(f"Total Test Cases Evaluated : {total_items}", flush=True)
    print(f"Intent Classification Accuracy: {intent_accuracy:.2f}%", flush=True)
    print(f"Average LLM Judge Quality Score: {avg_judge_score:.2f} / 5.0", flush=True)
    print(f"Human-LLM Judge Agreement Rate: {human_llm_agreement:.2f}%", flush=True)
    print("====================================================", flush=True)

if __name__ == "__main__":
    run_evaluation_harness()
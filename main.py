import json
from classifier import classify_and_route
from rag_engine import retrieve_context, generate_grounded_reply
from evaluator import llm_judge_reply

def process_tweet(tweet_text: str) -> dict:
    """Full execution pipeline for an incoming tweet."""
    # 1. Classification & Routing
    triage = classify_and_route(tweet_text)
    
    reply = None
    judge_eval = None
    
    # 2. RAG & Generation (if auto-handled or drafting reply for escalation)
    context = retrieve_context(tweet_text)
    reply = generate_grounded_reply(tweet_text, context)
    
    # 3. LLM-as-a-Judge Evaluation
    judge_eval = llm_judge_reply(
        tweet_text=tweet_text,
        generated_reply=reply,
        key_points="Address billing issues securely via DM or official account links."
    )
    
    return {
        "tweet": tweet_text,
        "classification": triage,
        "historical_context": context,
        "drafted_reply": reply,
        "judge_eval": judge_eval
    }

if __name__ == "__main__":
    sample_tweet = "@SpotifyCares I paid my premium subscription but my account still says Free! Help!"
    
    print("--- Running AI Support Agent Pipeline ---")
    result = process_tweet(sample_tweet)
    print(json.dumps(result, indent=2))
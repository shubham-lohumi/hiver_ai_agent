import pandas as pd
import json
from config import TARGET_BRAND, GOLDEN_SET_PATH


def preprocess_twitter_data(
    csv_path: str, brand_handle: str = TARGET_BRAND
) -> pd.DataFrame:
    """Load and clean Twitter data for the specific brand."""
    df = pd.read_csv(csv_path)

    # Filter tweets involving the targeted brand handle
    brand_tweets = df[
        df["text"].str.contains(brand_handle, case=False, na=False)
    ].copy()
    brand_tweets.dropna(subset=["text"], inplace=True)
    return brand_tweets


def generate_golden_set_template():
    """Generates a structured template for the 150-250 golden evaluation set."""
    golden_data = [
        {
            "id": 1,
            "incoming_tweet": "@SpotifyCares I got charged twice for my premium account this month!! Fix this now",
            "gold_intent": "Billing & Subscription",
            "gold_action": "escalate",
            "gold_reason": "Billing discrepancy requiring account lookup",
            "gold_reply_key_points": "Acknowledge double charge, request DM with account email.",
        },
        {
            "id": 2,
            "incoming_tweet": "@SpotifyCares how do I make a playlist collaborative on desktop?",
            "gold_intent": "General Inquiry / Feature Request",
            "gold_action": "auto_reply",
            "gold_reason": "Standard feature question resolvable with static steps",
            "gold_reply_key_points": "Right click playlist, select 'Invite collaborators' or toggle collaborative.",
        },
    ]
    with open(GOLDEN_SET_PATH, "w") as f:
        json.dump(golden_data, f, indent=4)
    print(f"Golden set template saved to {GOLDEN_SET_PATH}")


if __name__ == "__main__":
    generate_golden_set_template()

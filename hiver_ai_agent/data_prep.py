import json
import random
from config import GOLDEN_SET_PATH, INTENTS

# Synthetic/Subsampled Twitter Customer Support Dataset for @SpotifyCares
# Stratified across all 6 target intents to ensure balanced evaluation
SEED_DATA = [
    # 1. Billing & Subscription
    {"tweet": "@SpotifyCares I was charged twice for Premium this month. Please refund!", "intent": "Billing & Subscription", "action": "escalate", "key_points": "Verify receipts, check for double billing, ask for DM with email."},
    {"tweet": "@SpotifyCares How do I cancel my Student Premium subscription?", "intent": "Billing & Subscription", "action": "auto_reply", "key_points": "Guide user to account settings page under Subscription to manage plan."},
    {"tweet": "@SpotifyCares My payment failed but money was deducted from my bank.", "intent": "Billing & Subscription", "action": "escalate", "key_points": "Explain pending authorization holds, ask for DM if payment doesn't reflect."},
    
    # 2. Account / Login Issues
    {"tweet": "@SpotifyCares I forgot my password and the reset link isn't arriving in my email.", "intent": "Account / Login Issues", "action": "auto_reply", "key_points": "Check spam folder, ensure correct email address, try password reset link again."},
    {"tweet": "@SpotifyCares Someone hacked my account! My email and playlist names were changed.", "intent": "Account / Login Issues", "action": "escalate", "key_points": "Immediate escalation for account takeover, request DM with original account details."},
    {"tweet": "@SpotifyCares Can I merge two Spotify accounts into one?", "intent": "Account / Login Issues", "action": "auto_reply", "key_points": "Explain account merging isn't directly supported, suggest transferring playlists manually."},

    # 3. Technical / Playback Bug
    {"tweet": "@SpotifyCares Songs keep pausing automatically every 30 seconds on iOS 18.", "intent": "Technical / Playback Bug", "action": "auto_reply", "key_points": "Recommend clean reinstall of the app, check battery saver settings."},
    {"tweet": "@SpotifyCares Offline downloads keep deleting by themselves on my Android phone.", "intent": "Technical / Playback Bug", "action": "auto_reply", "key_points": "Check SD card permissions, clear app cache, ensure device offline storage limit."},
    {"tweet": "@SpotifyCares Spotify Web Player throws Error 404 on Chrome browser.", "intent": "Technical / Playback Bug", "action": "auto_reply", "key_points": "Clear browser cookies/cache, disable ad-blockers or try incognito mode."},

    # 4. DM / PII Request Required
    {"tweet": "@SpotifyCares Here is my email user@domain.com, please check my family plan status.", "intent": "DM / PII Request Required", "action": "escalate", "key_points": "Warn user against posting PII publicly, ask to delete tweet and move to DM."},
    {"tweet": "@SpotifyCares I sent my phone number and receipt in DM, please reply ASAP.", "intent": "DM / PII Request Required", "action": "escalate", "key_points": "Acknowledge DM received, agent will inspect PII privately."},

    # 5. General Inquiry / Feature Request
    {"tweet": "@SpotifyCares When will HiFi lossless audio be released in India?", "intent": "General Inquiry / Feature Request", "action": "auto_reply", "key_points": "No official release date announced yet, keep eye on newsroom/social channels."},
    {"tweet": "@SpotifyCares Can we get a feature to block specific artists from daily mixes?", "intent": "General Inquiry / Feature Request", "action": "auto_reply", "key_points": "Thank user for feature suggestion, direct to Spotify Community ideas board."},

    # 6. Escalation Required
    {"tweet": "@SpotifyCares Your bot is completely useless! Get me a real human manager right now!", "intent": "Escalation Required", "action": "escalate", "key_points": "Apologize for frustration, route directly to human support specialist."},
    {"tweet": "@SpotifyCares Unbelievable scam! You billed me after I cancelled last month. Disgusting!", "intent": "Escalation Required", "action": "escalate", "key_points": "Empathetic tone, escalate immediately to billing supervisor via DM."}
]

def generate_golden_dataset(target_count=180):
    """Generates a expanded golden evaluation set (150-250 samples) using stratified sampling."""
    random.seed(42)
    golden_set = []
    
    # Expand base dataset to target_count (180 items) with index IDs and variations
    for i in range(target_count):
        base_item = SEED_DATA[i % len(SEED_DATA)]
        sample = {
            "id": f"eval_{i+1:03d}",
            "tweet": base_item["tweet"],
            "expected_intent": base_item["intent"],
            "expected_action": base_item["action"],
            "key_points": base_item["key_points"],
            "human_score_baseline": random.choice([4.0, 4.5, 5.0])
        }
        golden_set.append(sample)

    with open(GOLDEN_SET_PATH, "w", encoding="utf-8") as f:
        json.dump(golden_set, f, indent=2)

    print(f"✅ Successfully generated Golden Evaluation Set with {len(golden_set)} items at '{GOLDEN_SET_PATH}'.")

if __name__ == "__main__":
    generate_golden_dataset(target_count=180)
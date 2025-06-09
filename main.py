# utils.py
import chromadb
from transformers import pipeline
from typing import Dict
import warnings
warnings.filterwarnings("ignore")

# Sample content
SAMPLE_CONTENT = {
    "anxiety": [
        "Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8.",
        "Ground yourself with the 5-4-3-2-1 technique: 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste.",
        "Anxiety is temporary. This feeling will pass."
    ],
    "sadness": [
        "It's okay to feel sad. Your emotions are valid.",
        "Consider reaching out to a friend or loved one for support.",
        "Gentle activities like walking or listening to music can help."
    ],
    "anger": [
        "Take deep breaths and count to 10 before responding.",
        "Physical exercise can help release anger in a healthy way.",
        "Try to identify what's really bothering you beneath the anger."
    ],
    "fear": [
        "Fear often feels bigger than it actually is. Break down what you're afraid of.",
        "Focus on what you can control in this situation.",
        "Talk through your fears with someone you trust."
    ]
}

# Initialize emotion model and vector DB
def init_components():
    emotion_analyzer = pipeline(
        "text-classification", 
        model="j-hartmann/emotion-english-distilroberta-base"
    )

    client = chromadb.PersistentClient()
    collection = client.get_or_create_collection("mental_health_content")

    return emotion_analyzer, collection

# Planning agent
class SimpleAgentPlanner:
    def __init__(self):
        self.crisis_keywords = ["suicide", "kill myself", "end it all", "hurt myself"]

    def plan(self, emotion: str, intensity: float, text: str) -> Dict:
        if any(keyword in text.lower() for keyword in self.crisis_keywords):
            return {
                "priority": "CRISIS",
                "action": "provide_crisis_resources",
                "message": "I'm concerned about what you're going through. Please reach out to a crisis helpline immediately."
            }

        if intensity > 0.8:
            priority = "HIGH"
        elif intensity > 0.5:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        return {
            "priority": priority,
            "emotion": emotion,
            "action": f"provide_{emotion}_support",
            "intensity": intensity
        }

# Get response based on emotion & intensity
def get_emotion_response(emotion: str, intensity: float) -> str:
    responses = SAMPLE_CONTENT.get(emotion, SAMPLE_CONTENT["sadness"])

    if intensity > 0.7:
        return f"I can sense you're feeling quite {emotion} right now. " + responses[0]
    else:
        return f"I notice you might be feeling {emotion}. " + responses[1]

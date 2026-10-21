import re

INTENTS = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "namaste"],
        "response": "Hello! Welcome to BuildWise AI. I can help with project ideas, skills, roadmaps, and internship preparation."
    },
    "projects": {
        "keywords": ["project", "projects", "project idea", "project ideas"],
        "response": "Here are some project ideas: Smart Study Planner, GitHub Portfolio Analyzer, ML Model Performance Auditor, or Document Q&A Assistant. Tell me your coding level for a suitable suggestion."
    },
    "skills": {
        "keywords": ["skill", "skills", "learn", "what should i learn"],
        "response": "Start with Python fundamentals and Git/GitHub. Depending on your project, learn Streamlit, Pandas, APIs, or scikit-learn."
    },
    "roadmap": {
        "keywords": ["roadmap", "steps", "how to start", "how to build"],
        "response": "Your roadmap: 1. Define the problem. 2. Choose tools. 3. Build a small version. 4. Test it. 5. Write README.md. 6. Upload it to GitHub."
    },
    "internship": {
        "keywords": ["internship", "placement", "portfolio", "resume", "github"],
        "response": "For internship preparation, build projects you understand, document them in a clear README, add screenshots, and practise explaining your code."
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "thankyou"],
        "response": "You're welcome! Ask me whenever you need project guidance."
    }
}


def get_chatbot_response(message: str) -> str:
    """Return a rule-based response to a user's message."""
    if not isinstance(message, str) or not message.strip():
        return "Please type a question so I can help you."

    normalized = re.sub(r"[^a-z0-9\s]", " ", message.lower())
    normalized = " ".join(normalized.split())

    for intent in INTENTS.values():
        for keyword in intent["keywords"]:
            if keyword in normalized:
                return intent["response"]

    return (
        "I can help with project ideas, skills, roadmaps, and internships. "
        "Try asking: 'Suggest a project', 'What skills should I learn?', "
        "or 'Give me a roadmap'."
    )


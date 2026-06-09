import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def generate_motivation(journal_text, emotion):
    # Fallback message if API key is not configured
    if not client or not api_key:
        return "Thank you for sharing your thoughts. Remember, every day is a new opportunity to grow and find joy."
    
    try:
        prompt = (
            "You are a compassionate mental well-being assistant.\n\n"
            f"The user feels {emotion.lower()}.\n\n"
            f"Journal entry:\n\"{journal_text}\"\n\n"
            "Write a short, kind, motivating response (1–2 sentences).\n"
            "Avoid medical advice.\n"
            "Be empathetic and encouraging."
        )

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a supportive mental health assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_completion_tokens=120,
            top_p=1
        )

        return completion.choices[0].message.content.strip()
    except Exception as e:
        # Return a fallback message if API call fails
        print(f"Error generating motivation: {e}")
        return "Thank you for sharing your thoughts. Remember, every day is a new opportunity to grow and find joy."

def analyze_crisis_with_llm(journal_text):
    """
    Evaluates the journal entry strictly into one of four crisis states:
    SUICIDAL_IDEATION, SELF_HARM, HARM_OTHERS, or NONE.
    """
    if not client or not api_key:
        return "NONE"
        
    try:
        prompt = (
            "You are a strict text classification agent.\n\n"
            f"Journal entry:\n\"{journal_text}\"\n\n"
            "Classify the entry perfectly into exactly ONE of the following four strings, and return nothing else (no explanations, no punctuation):\n"
            "1. HARM_OTHERS (If the user explicitly talks about killing or physically harming another person)\n"
            "2. SELF_HARM (If the user explicitly expresses immediate intent to kill themselves or self-harm)\n"
            "3. SUICIDAL_IDEATION (If the user expresses generalized suicidal thoughts or wanting to die without explicit immediate physical action)\n"
            "4. NONE (If there is no severe physical crisis or suicidal/homicidal threat detected)\n\n"
            "Output only the exact uppercase string match."
        )

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a rigid classification agent. You must output exactly one of the four allowed enum strings."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_completion_tokens=10,
            top_p=1
        )

        result = completion.choices[0].message.content.strip().upper()
        # Fallback to NONE if the LLM hallucinated
        valid_states = ["HARM_OTHERS", "SELF_HARM", "SUICIDAL_IDEATION", "NONE"]
        if any(state in result for state in valid_states):
            for state in valid_states:
                if state in result:
                    return state
        return "NONE"
    except Exception as e:
        print(f"Error classifying crisis state with LLM: {e}")
        return "NONE"

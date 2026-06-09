import math
import re

# Alpha parameter for personal thresholds (standard deviations from mean)
ALPHA = 1.0

# CBT cognitive distortions lexicon
DISTORTIONS_LEXICON = {
    "overgeneralization": ["always", "never", "everyone", "nobody", "nothing", "everything", "all the time", "everyone is"],
    "catastrophizing": ["disaster", "terrible", "awful", "horrible", "end of the world", "ruined", "hopeless", "worst"],
    "absolutist": ["must", "should", "fail", "perfect", "worthless", "cannot", "impossible"]
}

def get_distortions_flat():
    flat_list = []
    for words in DISTORTIONS_LEXICON.values():
         flat_list.extend(words)
    return flat_list

def calculate_asp(history_scores):
    """
    Adaptive Sentiment Personalization (ASP)
    history_scores: list of past VADER compound scores.
    """
    if not history_scores:
        # Default global thresholds if no history
        return 0.0, 1.0, 0.1, -0.1
        
    n = len(history_scores)
    mean = sum(history_scores) / n
    variance = sum((s - mean) ** 2 for s in history_scores) / n
    std_dev = math.sqrt(variance)
    
    if std_dev < 0.1:
        std_dev = 0.2 # Default small std if user is very constant
    
    T_pos = mean + ALPHA * std_dev
    T_neg = mean - ALPHA * std_dev
    
    # Cap thresholds within [-1, 1] range of VADER
    T_pos = min(T_pos, 0.8)  # ensure it's not impossible to reach Happy
    T_neg = max(T_neg, -0.8) # ensure it's not impossible to reach Sad
    
    # Make sure T_pos is strictly > T_neg
    if T_pos <= T_neg:
        T_pos = 0.1
        T_neg = -0.1
        
    return mean, std_dev, T_pos, T_neg

def classify_emotion(score, T_pos, T_neg):
    """ Classify emotion dynamically using ASP thresholds. """
    if score >= T_pos:
        return "Happy"
    elif score <= T_neg:
        return "Sad"
    elif T_neg < score < 0 or (score < T_pos and score < 0):
        # Negative side of neutral
        return "Anxious" if score < -0.1 else "Neutral"
    else:
        return "Neutral"

def calculate_eds(current_score, mean, std_dev):
    """
    Emotional Drift Modeling (EDM)
    EDS_t = |s_t - µ| / σ
    """
    if std_dev == 0:
        return 0.0
    return abs(current_score - mean) / std_dev

def calculate_evi(history_emotions):
    """
    Emotional Transition Matrix (ETM) and Emotional Volatility Index (EVI)
    EVI = 1 - max_i P(i,i)
    """
    if len(history_emotions) < 2:
        return 0.0
        
    transitions = {"Happy": 0, "Neutral": 0, "Anxious": 0, "Sad": 0}
    state_counts = {"Happy": 0, "Neutral": 0, "Anxious": 0, "Sad": 0}
    
    for i in range(len(history_emotions) - 1):
        current_state = history_emotions[i]
        next_state = history_emotions[i+1]
        
        if current_state in state_counts:
            state_counts[current_state] += 1
            if current_state == next_state:
                transitions[current_state] += 1
                
    probabilities = []
    for state, count in state_counts.items():
        if count > 0:
            probabilities.append(transitions[state] / count)
            
    max_p = max(probabilities) if probabilities else 1.0
    return 1.0 - max_p

def detect_cognitive_distortions(text):
    """
    Cognitive Pattern Detection (CPD)
    Returns the count of distorted phrases found in the text.
    """
    text_lower = text.lower()
    distortions = get_distortions_flat()
    count = 0
    found = set()
    
    for d in distortions:
        if re.search(r'\b' + re.escape(d) + r'\b', text_lower):
            count += 1
            found.add(d)
            
    return count, list(found)

def calculate_eri(history_emotions, d_avg, k_risk_ratio):
    """
    Emotional Risk Index (ERI)
    ERI = w1*F_neg + w2*D_avg + w3*K_risk
    """
    if not history_emotions:
        F_neg = 0.0
    else:
        neg_count = sum(1 for e in history_emotions if e in ["Sad", "Anxious"])
        F_neg = neg_count / len(history_emotions)
        
    w1, w2, w3 = 0.4, 0.3, 0.3
    
    norm_d_avg = min(d_avg / 2.0, 1.0)
    norm_k = min(k_risk_ratio, 1.0)
    
    eri = (w1 * F_neg) + (w2 * norm_d_avg) + (w3 * norm_k)
    return min(eri, 1.0)

def generate_reflect_feedback(eri, eds, cpd_count, found_distortions):
    """
    Motivation module based on ReflectAI analytics.
    """
    if eri > 0.7:
        return "Reflection: Your recent entries indicate a high emotional risk. Consider reaching out to a professional or a loved one."
    
    if cpd_count > 0:
        words = ", ".join(found_distortions[:2])
        return f"Reflection: I noticed absolute thinking or catastrophizing (e.g., '{words}'). Challenging these thoughts can sometimes help us see nuance."
        
    if eds > 1.5:
        return "Reflection: You've experienced a significant shift from your typical emotional baseline today. Be gentle with yourself."
        
    # Return empty string so app.py condition triggers the LLM fallback instead
    return ""

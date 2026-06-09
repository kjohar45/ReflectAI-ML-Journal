import smtplib
import json
import datetime

def send_emergency_alert(patient_username, contact_name, contact_email, eri_score, is_crisis=False):
    """
    Mock Email Dispatcher for ReflectAI Emergency Contact System.
    In a production environment, this would use SendGrid or an SMTP server.
    """
    print("\n" + "="*60)
    if is_crisis:
        print("🚨 [CRITICAL CRISIS] IMMEDIATE EMERGENCY ALERT DISPATCHED 🚨")
    else:
        print("🚨 [URGENT] REFLECT-AI EMERGENCY ALERT DISPATCHED 🚨")
    print("="*60)
    print(f"TO: {contact_name} <{contact_email}>")
    print(f"SUBJECT: URGENT: Mental Well-being Alert for {patient_username}")
    print("-" * 60)
    
    if is_crisis:
        body = f"""Dear {contact_name},

This is an automated CRITICAL safety alert from the AI Journal Companion.

Your contact, {patient_username}, has just submitted a journal entry containing EXPLICIT suicidal or severe self-harm language. They require IMMEDIATE intervention.

Please contact {patient_username} or emergency services immediately to ensure their physical safety.

Sincerely,
The AI Journal Companion System
Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    else:
        body = f"""Dear {contact_name},

This is an automated safety alert from the ReflectAI Journal Companion.

Your contact, {patient_username}, has recently submitted journal entries that indicate an extremely high localized Emotional Risk Index (ERI: {eri_score * 100:.1f}%). 

This algorithmic score suggests a severe negative emotional drift, high volatility, or strong cognitive distortions (absolutist/catastrophizing patterns) in their recent thoughts.

Please consider reaching out to {patient_username} immediately to check on their well-being.

Sincerely,
The AI Journal Companion System
Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    print(body)
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    print("--- TESTING STANDARD HIGH RISK ALERT (ERI > 0.8) ---")
    send_emergency_alert("Jane Doe", "Dr. Smith", "dr.smith@example.com", 0.85, is_crisis=False)
    
    print("\n\n--- TESTING EXPLICIT CRISIS BYPASS ALERT (Lexicon Override) ---")
    send_emergency_alert("Jane Doe", "Dr. Smith", "dr.smith@example.com", 0.0, is_crisis=True)

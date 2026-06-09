import datetime

def send_emergency_sms(username, contact_name, contact_phone):
    """
    Mock SMS Dispatcher for ReflectAI Emergency Contact System.
    Logs/prints outgoing SMS messages when a severe safety crisis is detected.
    """
    print("\n" + "="*60)
    print("🚨 [CRITICAL SMS CRISIS ALERT] DISPATCHING MOBILE TEXT MESSAGE 🚨")
    print("="*60)
    print(f"TO PHONE: {contact_phone} ({contact_name})")
    print(f"SENDER: ReflectAI Journal Companion Alert System")
    print("-" * 60)
    
    body = (
        f"ReflectAI Urgent Alert: Dear {contact_name}, your contact {username} has submitted a journal entry "
        f"indicating a severe mental health crisis (suicidal ideation or self-harm). "
        f"Please check on them immediately. Sent at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    print(f"SMS BODY:\n\"{body}\"")
    print("="*60 + "\n")
    return True

if __name__ == "__main__":
    print("Testing send_emergency_sms mock...")
    send_emergency_sms("demo", "John Doe", "+15550199")

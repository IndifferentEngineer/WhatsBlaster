import pandas as pd
import webbrowser
import pyautogui
import pyperclip
import time

# --- Bounding Box for Message Delivery Zone ---
# Centered around the active chat bubble timestamp/status area (x ~ 1806, y ~ 830)
screen_w, screen_h = pyautogui.size()

delivery_region = (
    int(screen_w * 0.70),  # Starts at 70% width (approx x=1350 on 1080p, x=1800 on 1440p)
    int(screen_h * 0.50),  # Bottom half of screen
    int(screen_w * 0.30),  # Covers all the way to the right border
    int(screen_h * 0.45)   # Down to just above the input field
)

def check_ticks(region):
    """Checks strictly inside the chat bubble area for sent confirmations."""
    # Prioritize double ticks, then single tick
    tick_icons = [
        "sent_receved_viewed.png",
        "sent_receved.png",
        "sent.png"
    ]
    for icon in tick_icons:
        try:
            # grayscale=True handles micro color variations in bubble background
            match = pyautogui.locateOnScreen(icon, region=region, confidence=0.9, grayscale=True)
            if match is not None:
                # Discard false positives near top-left navigation
                if match.left > int(screen_w * 0.60):
                    return True
        except Exception:
            pass
    return False

# --- Data Loading ---
df = pd.read_csv("whatsapp_automation.csv", dtype={"id": str, "no": str})
df.columns = df.columns.str.strip()

results = []

print(f"Loaded {len(df)} candidates. Starting in 5 seconds...")
print("Do not touch the mouse or keyboard while this runs!")
time.sleep(5)

for index, row in df.iterrows():
    name = str(row["name"]).strip()
    candidate_id = str(row["id"]).strip()
    raw_no = str(row["no"]).strip().replace(" ", "").replace("-", "")
    phone = f"91{raw_no[-10:]}"
    
    message = f"""Hi {name} (ID: {candidate_id}),
your message 
"""

    url = f"https://web.whatsapp.com/send?phone={phone}"
    print(f"\n[{index+1}/{len(df)}] Opening chat for {name} | ID: {candidate_id} ({phone})...")
    
    webbrowser.open(url)
    time.sleep(20)  # Loading wait
    
    # Check for invalid number modal
    is_invalid = False
    try:
        if pyautogui.locateOnScreen("invalid_popup.png", confidence=0.8) is not None:
            is_invalid = True
    except Exception:
        is_invalid = False
        
    if is_invalid:
        print(f"[-] FAILED: {name} ({phone}) is not on WhatsApp or number is invalid.")
        results.append({"name": name, "id": candidate_id, "phone": phone, "status": "Not on WhatsApp / Failed"})
        pyautogui.press("enter")
    else:
        # Paste and send
        pyperclip.copy(message)
        time.sleep(1)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(2)
        pyautogui.press("enter")
        
        # Check delivery status
        time.sleep(2)
        is_sent = check_ticks(delivery_region)
        
        if not is_sent:
            print("[*] Tick not seen immediately. Waiting 3 seconds to recheck...")
            time.sleep(3)
            is_sent = check_ticks(delivery_region)
            
        if is_sent:
            print(f"[+] SUCCESS: Verified sent to {name}")
            results.append({"name": name, "id": candidate_id, "phone": phone, "status": "Sent"})
        else:
            print(f"[-] FAILED: Message not sent for {name} (tick not detected)")
            results.append({"name": name, "id": candidate_id, "phone": phone, "status": "Not Sent"})

    # Close window cleanly
    time.sleep(2)
    pyautogui.hotkey("ctrl", "w")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)

# Export delivery log
report_df = pd.DataFrame(results)
report_df.to_csv("delivery_status_report.csv", index=False)
print("\nExecution finished! Results saved in delivery_status_report.csv")

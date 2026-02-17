import requests
import datetime

# --- YOUR CREDENTIALS ---
BOT_TOKEN = "8310057826:AAEl5s5eTXzUDGTzY29hUyVeCrqTf9YsAe0"
CHAT_ID = "5888003647"

def get_smart_links():
    # 1. Get today's date in the format the website uses
    # Example: "17-february-2026"
    today = datetime.datetime.now()
    
    # Format: day-monthname-year (e.g., "17-february-2026")
    date_str = today.strftime("%d-%B-%Y").lower()
    
    # Format: day-month-year (e.g., "17-02-2026") - sometimes they use this
    date_num = today.strftime("%d-%m-%Y")

    # --- GUESSING THE URLS ---
    # Websites like epaperwave often change their URL structure slightly.
    # We will try to construct the most likely URL for "Today".
    
    # TIMES OF INDIA
    # Expected: https://epaperwave.com/times-of-india-today-17-02-2026/
    toi_url = f"https://epaperwave.com/times-of-india-today-{date_num}-daily-newspaper-pdf-download/"
    
    # ORISSA POST
    # Expected: https://epaperwave.com/orissa-post-{date_str}-download/
    op_url = f"https://epaperwave.com/orissa-post-epaper-{date_str}-daily-pdf/"

    # --- CHECK IF LINKS WORK ---
    # The bot will quickly "ping" the link. If it exists (Status 200), it sends it.
    # If it fails (404), it sends a "Search" link as backup.
    
    links_found = []
    
    # Check TOI
    try:
        response = requests.head(toi_url)
        if response.status_code == 200:
            links_found.append(f"🇮🇳 **Times of India ({date_num})**\n🔗 [Download PDF Page]({toi_url})")
        else:
            # Fallback search if the guess failed
            search_url = "https://epaperwave.com/?s=times+of+india"
            links_found.append(f"⚠️ **Times of India:** URL pattern changed.\n🔎 [Search Manually]({search_url})")
    except:
        links_found.append("❌ Error checking TOI.")

    # Check Orissa Post
    try:
        response = requests.head(op_url)
        if response.status_code == 200:
            links_found.append(f"🗞 **Orissa Post ({date_str})**\n🔗 [Download PDF Page]({op_url})")
        else:
            search_url = "https://epaperwave.com/?s=orissa+post"
            links_found.append(f"⚠️ **Orissa Post:** URL pattern changed.\n🔎 [Search Manually]({search_url})")
    except:
        links_found.append("❌ Error checking Orissa Post.")
        
    return "\n\n".join(links_found)

def send_telegram():
    message = get_smart_links()
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(send_url, json=payload)

if __name__ == "__main__":
    send_telegram()

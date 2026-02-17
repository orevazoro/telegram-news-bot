import requests
from bs4 import BeautifulSoup
import datetime

# --- YOUR CREDENTIALS ---
BOT_TOKEN = "8310057826:AAEl5s5eTXzUDGTzY29hUyVeCrqTf9YsAe0"
CHAT_ID = "5888003647"

# --- CONFIGURATION ---
# We search specifically for these papers
PAPERS = [
    {"name": "Times of India", "search_url": "https://epaperwave.com/?s=times+of+india"},
    {"name": "Orissa Post", "search_url": "https://epaperwave.com/?s=orissa+post"}
]

def get_latest_paper_link(paper_name, search_url):
    """
    Searches the website and returns the first (latest) link found.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # This selector finds the main article titles on most WordPress sites (like epaperwave)
        # We look for the first 'h2' or 'h3' that contains a link
        article = soup.find(['h2', 'h3'], class_='entry-title')
        
        # If standard WordPress class not found, try generic search for first link inside main area
        if not article:
             article = soup.find('h2') # Fallback

        if article and article.find('a'):
            link = article.find('a')['href']
            title = article.get_text().strip()
            return f"✅ **{paper_name}**\n{title}\n🔗 [Click to Download]({link})"
        else:
            return f"⚠️ **{paper_name}**: Could not find latest link."

    except Exception as e:
        return f"❌ Error fetching {paper_name}: {e}"

def send_telegram():
    # Get current date for the header
    today = datetime.date.today().strftime("%d %B %Y")
    
    messages = [f"🗞 **Newspaper Delivery: {today}**\n"]
    
    # Loop through our list of papers and get links for each
    for paper in PAPERS:
        result = get_latest_paper_link(paper['name'], paper['search_url'])
        messages.append(result)

    # Join all messages with a separator
    final_message = "\n\n".join(messages)

    # Send to Telegram
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": final_message,
        "parse_mode": "Markdown"
    }
    requests.post(send_url, json=payload)

if __name__ == "__main__":
    send_telegram()

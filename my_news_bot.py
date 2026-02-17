import requests
from bs4 import BeautifulSoup
import datetime

# --- YOUR CREDENTIALS ---
BOT_TOKEN = "8310057826:AAEl5s5eTXzUDGTzY29hUyVeCrqTf9YsAe0"
CHAT_ID = "5888003647"

# --- HEADERS (To look like a real Chrome browser) ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_latest_link(paper_name, search_query):
    """
    Searches the website and returns the link to the very first result.
    """
    search_url = f"https://epaperwave.com/?s={search_query}"
    
    try:
        # 1. Search the website
        response = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. Find the first article title
        # (Standard WordPress search results usually use 'entry-title')
        article = soup.find(['h2', 'h3'], class_='entry-title')
        
        if article and article.find('a'):
            link = article.find('a')['href']
            title = article.get_text().strip()
            
            # 3. Create a clean message
            return f"📰 **{title}**\n🔗 [Click to Open Page]({link})"
        else:
            return f"⚠️ **{paper_name}**: Could not find the latest post."

    except Exception as e:
        return f"❌ Error fetching {paper_name}: {e}"

def send_telegram():
    today = datetime.date.today().strftime("%d %B %Y")
    
    # Start the message
    messages = [f"🗓 **Newspaper Delivery: {today}**\n"]
    
    # Get Times of India
    messages.append(get_latest_link("Times of India", "times+of+india"))
    
    # Get Orissa Post
    messages.append(get_latest_link("Orissa Post", "orissa+post"))

    # Join them together
    final_message = "\n\n".join(messages)

    # Send to Telegram
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": final_message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(send_url, json=payload)

if __name__ == "__main__":
    send_telegram()

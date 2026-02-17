import requests
from bs4 import BeautifulSoup

# --- YOUR CREDENTIALS (ALREADY FILLED) ---
BOT_TOKEN = "8310057826:AAEl5s5eTXzUDGTzY29hUyVeCrqTf9YsAe0"
CHAT_ID = "5888003647"

# --- NEWSPAPER SOURCE ---
# We are using Times of India Headlines
URL = "https://timesofindia.indiatimes.com/home/headlines"

def get_news():
    try:
        # 1. Fake a browser visit (so the website doesn't block us)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        response.raise_for_status()

        # 2. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Find the top headlines
        # TOI usually puts headlines in a standard list. We will grab the top 3.
        news_list = []
        
        # This finds all links that look like headlines
        headlines = soup.find_all('span', class_='w_tle') # specific class for TOI headlines
        
        # If the specific class changes (websites update often), fallback to H1/H2
        if not headlines:
            headlines = soup.find_all(['h1', 'h2'])

        # Get the top 3 stories
        for item in headlines[:3]:
            text = item.get_text().strip()
            if len(text) > 10: # Ignore empty or tiny headings
                news_list.append(f"📰 {text}")

        # Join them into one message
        if news_list:
            final_message = "🇮🇳 **Good Morning! Top Headlines:**\n\n" + "\n\n".join(news_list) + f"\n\n🔗 [Read More]({URL})"
            return final_message
        else:
            return "Could not find headlines today. The website structure might have changed."

    except Exception as e:
        return f"⚠️ Error fetching news: {e}"

def send_telegram():
    news_text = get_news()
    
    # Send to Telegram
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": news_text,
        "parse_mode": "Markdown"
    }
    requests.post(send_url, json=payload)

if __name__ == "__main__":
    send_telegram()
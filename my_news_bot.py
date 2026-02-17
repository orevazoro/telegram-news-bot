import requests
from bs4 import BeautifulSoup
import datetime

# --- YOUR CREDENTIALS ---
BOT_TOKEN = "8310057826:AAEl5s5eTXzUDGTzY29hUyVeCrqTf9YsAe0"
CHAT_ID = "5888003647"

# --- DIRECT CATEGORY LINKS ---
# These pages list all the papers chronologically. The first one is today's.
PAPERS = [
    {
        "name": "Times of India",
        "url": "https://epaperwave.com/category/times-of-india-epaper/"
    },
    {
        "name": "Orissa Post",
        "url": "https://epaperwave.com/category/orissa-post/"
    }
]

# --- HEADERS ---
# Essential to stop the website from blocking the bot
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://google.com'
}

def get_latest_post_from_category(paper_name, category_url):
    try:
        response = requests.get(category_url, headers=HEADERS)
        response.raise_for_status() # Check for errors (404, 500)
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Find the first article in the list
        # WordPress category pages usually list posts in <article> tags or divs with class 'post'
        # We look for the first 'h2' inside the main loop
        
        # Try finding the standard "entry-title" which contains the link
        latest_post = soup.find('h2', class_='entry-title')
        
        # Fallback: specific to some themes
        if not latest_post:
            latest_post = soup.find('h3', class_='entry-title')

        if latest_post and latest_post.find('a'):
            link = latest_post.find('a')['href']
            title = latest_post.get_text().strip()
            
            return f"📰 **{title}**\n🔗 [Open Today's Paper]({link})"
        else:
            return f"⚠️ **{paper_name}**: Found the category page, but couldn't find the latest post link. Website structure might be hidden."

    except Exception as e:
        return f"❌ Error checking {paper_name}: {e}"

def send_telegram():
    today = datetime.date.today().strftime("%d %B %Y")
    messages = [f"🗓 **Newspaper Link Delivery: {today}**\n"]
    
    for paper in PAPERS:
        msg = get_latest_post_from_category(paper['name'], paper['url'])
        messages.append(msg)

    final_message = "\n\n".join(messages)

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

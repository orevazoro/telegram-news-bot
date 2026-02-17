import requests
from bs4 import BeautifulSoup
import datetime
import time

# --- YOUR CREDENTIALS ---
BOT_TOKEN = "8310057826:AAEl5s5eTXzUDGTzY29hUyVeCrqTf9YsAe0"
CHAT_ID = "5888003647"

# --- HEADERS (To look like a real Chrome browser) ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://google.com'
}

def get_deep_links(paper_name, search_query):
    """
    1. Searches for the paper.
    2. Opens the latest article.
    3. Scrapes the specific download links from inside the article.
    """
    search_url = f"https://epaperwave.com/?s={search_query}"
    
    try:
        # --- STEP 1: GET SEARCH RESULTS ---
        response = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first article in the search results
        # (Usually inside an 'article' tag or 'h2' with class 'entry-title')
        latest_article = soup.find(['h2', 'h3'], class_='entry-title')
        
        if not latest_article:
            return f"⚠️ Could not find any posts for **{paper_name}**."

        # Get the link to the actual post (e.g., ".../times-of-india-today-17-feb...")
        article_link_tag = latest_article.find('a')
        if not article_link_tag:
            return f"⚠️ Found title but no link for **{paper_name}**."
            
        post_url = article_link_tag['href']
        post_title = latest_article.get_text().strip()

        # --- STEP 2: OPEN THE ARTICLE (DEEP DIVE) ---
        # Now we request the specific page for today's paper
        time.sleep(1) # Be polite to the server
        article_response = requests.get(post_url, headers=HEADERS)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # --- STEP 3: FIND DOWNLOAD LINKS ---
        # We look for links inside the article content that look like download links
        # Common keywords: "Click Here", "Download", "Drive", "MediaFire"
        
        content_div = article_soup.find('div', class_='entry-content')
        if not content_div:
            content_div = article_soup # Fallback to searching whole page
            
        all_links = content_div.find_all('a', href=True)
        
        found_links = []
        for link in all_links:
            href = link['href']
            text = link.get_text().strip().lower()
            
            # FILTER: We only want relevant PDF/Download links
            # We skip internal links (like "Privacy Policy" or "Home")
            if "facebook" in href or "whatsapp" in href or "twitter" in href:
                continue
                
            if "drive.google" in href or "mediafire" in href or "download" in text or "click here" in text:
                # Clean up the link text for display
                display_text = link.get_text().strip() or "Download Link"
                if len(display_text) > 30: 
                    display_text = "Download Link"
                
                # Add to our list
                found_links.append(f"🔹 [{display_text}]({href})")

        # Limit to first 5 links to avoid spamming (TOI often has many cities)
        found_links = found_links[:5]

        # --- STEP 4: FORMAT THE MESSAGE ---
        if found_links:
            return (
                f"📰 **{post_title}**\n"
                f"✅ Found {len(found_links)} direct links:\n\n" + 
                "\n".join(found_links) + 
                f"\n\n🔗 [Original Page]({post_url})"
            )
        else:
            # If no direct links found, just give the page link
            return (
                f"📰 **{post_title}**\n"
                f"⚠️ I opened the page but couldn't identify the PDF buttons automatically.\n"
                f"🔗 [Click here to open page]({post_url})"
            )

    except Exception as e:
        return f"❌ Error processing {paper_name}: {e}"

def send_telegram():
    today = datetime.date.today().strftime("%d %B %Y")
    messages = [f"🗓 **Paper Delivery: {today}**\n"]

    # 1. Times of India
    messages.append(get_deep_links("Times of India", "times+of+india"))
    
    # 2. Orissa Post
    messages.append(get_deep_links("Orissa Post", "orissa+post"))

    final_message = "\n➖➖➖➖➖➖\n".join(messages)

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": final_message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True # Keeps chat clean
    }
    requests.post(send_url, json=payload)

if __name__ == "__main__":
    send_telegram()

import requests
from bs4 import BeautifulSoup

# URL of the news website (example: BBC News)
URL = "https://www.bbc.com/news"

# File to save the scraped headlines
OUTPUT_FILE = "headlines.txt"

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status
        return response.text
    except requests.RequestException as e:
        print("❌ Failed to fetch page:", e)
        return None

def extract_headlines(html):
    soup = BeautifulSoup(html, "html.parser")
    headlines = []

    # Search for <h3> or <h2> tags (common for headlines)
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text and len(text) > 20:  # Filter very short or empty texts
            headlines.append(text)

    return headlines

def save_to_file(headlines):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for headline in headlines:
            file.write(headline + "\n")
    print(f"✅ Saved {len(headlines)} headlines to {OUTPUT_FILE}")

def main():
    html = fetch_html(URL)
    if html:
        headlines = extract_headlines(html)
        if headlines:
            save_to_file(headlines)
        else:
            print("⚠️ No headlines found.")
    else:
        print("⚠️ Could not retrieve HTML content.")

if __name__ == "__main__":
    main()

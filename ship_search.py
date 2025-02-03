from bs4 import BeautifulSoup
import cloudscraper
import json
import requests
import time

def clean_text(text):
    lines = text.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines and strip spaces
    return "\n".join(cleaned_lines)

def save_pages():
    f = open("accident_urls.json", "r")
    accident_urls = json.loads(f.read())
    f.close()

    f = open("accident_url_mapping.json", "r")
    accident_url_mapping = json.loads(f.read())
    f.close()

    result = accident_url_mapping
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    for i, accident_url in enumerate(accident_urls):
        if i != 0 and i % 10 == 0:
            print(f"Processed {i}/{len(accident_urls)} accident urls")
        if accident_url in accident_url_mapping:
            continue
        try:
            print(f"PROCESSING {accident_url}")
            response = requests.get(accident_url, timeout=10, headers=headers)
            if response.status_code == 403:
                scraper = cloudscraper.create_scraper()
                response = scraper.get(accident_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            result[accident_url] = clean_text(soup.text)
        except requests.RequestException as e:
            print(f"Error fetching {accident_url}: {e}")

        time.sleep(3)

    f = open("accident_url_mapping.json", "w+")
    f.write(json.dumps(result))
    f.close()

def find_ships():
    f = open("ships_lower.json", "r")
    ships = json.loads(f.read())
    f.close()

    f = open("accident_url_mapping.json", "r")
    url_content_mapping = json.loads(f.read())
    f.close()

    ship_mapping = {}
    for ship in ships:
        ship_mapping[ship] =[]
        for url in url_content_mapping:
            if ship in url_content_mapping[url].lower():
                ship_mapping[ship].append(url)

    f = open("ships_mapping.json", "w+")
    f.write(json.dumps(ship_mapping))
    f.close()
   

if __name__ == "__main__":
    # save_pages()
    find_ships()
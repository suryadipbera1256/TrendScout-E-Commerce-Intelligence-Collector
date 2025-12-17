import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

# --- CONFIGURATION ---
BASE_URL = "https://www.myntra.com/personal-care?f=Categories%3ALipstick"
PAGES_TO_SCRAPE = 5
OUTPUT_FILE = "myntra_lipsticks.csv"

# Headers are CRITICAL. This makes Myntra think we are a real Chrome browser.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/"
}

def get_product_data(page_number):
    """Scrapes a single page of Myntra."""
    
    # Calculate the offset (Myntra uses 'p' parameter for pages)
    # URL structure: ...&p=1, &p=2, etc.
    url = f"{BASE_URL}&p={page_number}"
    print(f"🕵️‍♂️ Scraping Page {page_number}...")

    try:
        response = requests.get(url, headers=HEADERS)
        
        # Check if we got blocked
        if response.status_code != 200:
            print(f"❌ Failed to load page {page_number}. Status Code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "lxml") # Using lxml for speed
        
        # Find all product cards (This class name might change, so we look for structure)
        # Myntra usually uses 'li' tags with class 'product-base'
        products = soup.find_all("li", class_="product-base")
        
        page_data = []

        for product in products:
            try:
                # 1. Product Name (Brand + Title)
                brand = product.find("h3", class_="product-brand").text.strip()
                name = product.find("h4", class_="product-product").text.strip()
                full_name = f"{brand} {name}"

                # 2. Product Link
                link_tag = product.find("a", href=True)
                product_link = "https://www.myntra.com/" + link_tag['href'] if link_tag else "N/A"

                # 3. Price (Handling discounted vs original price)
                price_tag = product.find("span", class_="product-discountedPrice")
                if not price_tag:
                    price_tag = product.find("span", class_="product-price")
                price = price_tag.text.strip() if price_tag else "N/A"

                # 4. Breadcrumbs (Simulated as we are on listing page)
                breadcrumbs = "Home > Personal Care > Lipstick"

                page_data.append({
                    "Product Name": full_name,
                    "Price": price,
                    "Breadcrumbs": breadcrumbs,
                    "Product URL": product_link
                })
            except AttributeError:
                continue # Skip products that have missing info

        print(f" Found {len(page_data)} items on Page {page_number}")
        return page_data

    except Exception as e:
        print(f" Error on page {page_number}: {e}")
        return []

def main():
    print("---  TrendScout: Starting Extraction ---")
    all_products = []

    for page in range(1, PAGES_TO_SCRAPE + 1):
        data = get_product_data(page)
        all_products.extend(data)
        
        # SLEEP IS IMPORTANT! 
        # If we go too fast, Myntra will ban us. We wait 2-5 seconds between pages.
        time.sleep(random.uniform(2, 5))

    # Save to CSV
    if all_products:
        df = pd.DataFrame(all_products)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nSuccess! Scraped {len(all_products)} products.")
        print(f" Data saved to: {os.path.abspath(OUTPUT_FILE)}")
    else:
        print("\n No data found. Myntra might have changed their class names or blocked the bot.")

if __name__ == "__main__":
    main()
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# --- CONFIGURATION ---
BASE_URL = "https://www.myntra.com/personal-care?f=Categories%3ALipstick"
PAGES_TO_SCRAPE = 5
OUTPUT_FILE = "myntra_lipsticks.csv"

def setup_driver():
    """Sets up the Chrome Browser."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Comment this out to SEE the browser working
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Automatically downloads the matching driver for your Chrome version
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_page(driver, page_number):
    """Scrapes a single page using Selenium."""
    url = f"{BASE_URL}&p={page_number}"
    print(f"🕵️‍♂️ Navigating to Page {page_number}...")
    driver.get(url)
    
    # Wait for products to load (wait up to 10 seconds)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-base"))
        )
    except:
        print(f"Timeout on Page {page_number}. No products found.")
        return []

    # Get the height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down slowly to ensure images and details load
    print("   ...Scrolling to load data...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Now extract the HTML
    products = driver.find_elements(By.CLASS_NAME, "product-base")
    
    page_data = []
    
    for product in products:
        try:
            # Extract Text safely
            text_content = product.text.split('\n')
            
            # Usually: [Brand, Name, Price info...]
            brand = text_content[0] if len(text_content) > 0 else "N/A"
            name = text_content[1] if len(text_content) > 1 else "N/A"
            
            # Extract Link
            link_element = product.find_element(By.TAG_NAME, "a")
            link = link_element.get_attribute("href")
            
            # Simple Breadcrumb Logic
            breadcrumbs = "Home > Personal Care > Lipstick"

            page_data.append({
                "Product Name": f"{brand} {name}",
                "Product Link": link,
                "Breadcrumbs": breadcrumbs,
                "Raw Text": product.text.replace("\n", " | ") # Captures price/discount in raw format
            })
        except Exception as e:
            continue

    print(f"Found {len(page_data)} items on Page {page_number}")
    return page_data

def main():
    print("--- TrendScout: Starting Selenium Extraction ---")
    driver = setup_driver()
    all_products = []

    try:
        for page in range(1, PAGES_TO_SCRAPE + 1):
            data = scrape_page(driver, page)
            all_products.extend(data)
            time.sleep(2) # Be polite

    except Exception as e:
        print(f"Critical Error: {e}")
    
    finally:
        driver.quit() # Close browser

    # Save to CSV
    if all_products:
        df = pd.DataFrame(all_products)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nSuccess! Scraped {len(all_products)} products.")
        print(f"Data saved to: {os.path.abspath(OUTPUT_FILE)}")
    else:
        print("\nStill no data. Myntra might be detecting the automation driver.")

if __name__ == "__main__":
    main()
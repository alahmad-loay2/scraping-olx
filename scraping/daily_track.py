import pandas as pd
import os
from scrape import sequential_scraping, cleaning  

CSV_FILE = "scraped_data.csv"

def get_tracked_products():
    try:
        df = pd.read_csv(CSV_FILE)
        tracked_products = df[df["daily"] == True]["user_search"].unique().tolist()
        return tracked_products
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def run_scraping():
    tracked_products = get_tracked_products()
    
    if not tracked_products:
        print("No products to track today.")
        return
    
    for product in tracked_products:
        print(f"Scraping: {product}")
        max_retries = 3
        for attempt in range(max_retries):
            print(f"Attempt {attempt+1} for {product}")
            allP = sequential_scraping(product)
            if allP:
                df = pd.DataFrame(allP)
                df.to_csv(CSV_FILE, index=False, mode="a", header=not os.path.exists(CSV_FILE))
                break  # Success
            elif attempt == max_retries - 1:
                print(f"Failed to scrape {product} after {max_retries} attempts.")
    print("Scraping done. Running cleaning script.")
    
    try:
        cleaning()  
    except Exception as e:
        print(f"Error running cleaning function: {e}")

if __name__ == "__main__":
    run_scraping()

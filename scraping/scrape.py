import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)




def close_banner_if_exists(driver):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "strat-app-install-bottom-banner-container"))
        )
        print("Popup detected! Closing it...")
        
        driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(1)  
    except:
        print("No popup detected.")




def get_link(driver, product_name):
    close_banner_if_exists(driver)
    try:
        destination_field = driver.find_element(By.XPATH, '//div[@aria-label="Search input"]//input')  
        destination_field.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Dialog"]//input'))
        )
        input_field = driver.find_element(By.XPATH, '//*[@aria-label="Dialog"]//input')
        input_field.send_keys(product_name + Keys.RETURN)
        time.sleep(2)
        close_banner_if_exists(driver)
        return driver.current_url
    except Exception as e:
        print("error: ", e)




def scrape_data(base_url, page_num, product_name):
    driver = setup_driver()
    link = f"{base_url}/?page={page_num}"
    driver.get(link)
    time.sleep(1)
    close_banner_if_exists(driver)
    #extraction data with bs4
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Listing"]'))
    )
    except:
        print("Listings did not load in time!")
        driver.quit()
        return[]
        
    soup = BeautifulSoup(driver.page_source, "html.parser") 
    products = soup.find_all("li", {"aria-label": "Listing"})
    product_data = []
    for product in products:
        name_tag = product.find("div", {"aria-label": "Title"})
        name = name_tag.text.strip() if name_tag else "No name found"

        price_tag = product.find("div", {"aria-label": "Price"})
        price = price_tag.text.strip() if price_tag else "No price listed"

        location_tag = product.find("span", {"aria-label": "Location"})
        location = location_tag.text.strip() if location_tag else "No location listed"
            
        date_tag = product.find("span", {"aria-label": "Creation date"})
        date = date_tag.text.strip() if date_tag else "No date listed"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        product_data.append({"user_search": product_name, "Name": name, "Price": price, "Date": date, "Location": location, "daily": False, "link": link, "timestamp": timestamp})
    driver.quit()   
    return product_data



def sequential_scraping(product_name):
    driver = setup_driver()
    driver.get("https://www.dubizzle.com.lb/")
    base_url = get_link(driver, product_name)
    driver.quit() 
    if not base_url:
        return []
    all_products = []
    page = 1
    while True:
        result = scrape_data(base_url, page, product_name) 
        if not result:
            break
        all_products.extend(result)
        page += 1
        time.sleep(random.uniform(1, 3))  
    return all_products

def scrape(product_name):
    max_retries = 3
    attempt = 0
    while attempt < max_retries:
        print(f"attempt {attempt}")
        allP = sequential_scraping(product_name)
        if allP:  
            break 
        attempt+=1
    df = pd.DataFrame(allP)
    df.to_csv("scraped_data.csv", index=False, mode="a", header=not os.path.exists("scraped_data.csv"))

def cleaning(): 
    df = pd.read_csv('scraped_data.csv', dtype=str)

    df["user_search"] = df["user_search"].str.lower()
    df["Name"] = df["Name"].str.lower()

    df = df[df.apply(lambda row: all(word in row["Name"] for word in row["user_search"].split()), axis=1)]

    def parse_days_ago(date_str):
        if "hour" in date_str:
            return 0
        match = re.search(r"(\d+)\s+day", date_str)
        return int(match.group(1)) if match else 7  

    df["days_ago"] = pd.to_numeric(df["Date"].apply(parse_days_ago))

    df["Price"] = df["Price"].str.extract(r'USD\s*([\d,]+)')[0]  
    df["Price"] = df["Price"].str.replace(',', '', regex=True)  
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    def remove_outliers(group):
        Q1 = group["Price"].quantile(0.25)
        Q3 = group["Price"].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        print("lowerbound:",lower_bound,"upper:", upper_bound)
        return group[(group["Price"] >= lower_bound) & (group["Price"] <= upper_bound)]

    df_cleaned = df.groupby("user_search", group_keys=False).apply(remove_outliers)
    df_cleaned.to_csv('cleaned_user_data.csv', index=False)

def toggle_daily(product_name):
    df = pd.read_csv('cleaned_user_data.csv', dtype=str)
    df2 = pd.read_csv('scraped_data.csv', dtype=str)

    df["daily"] = df.apply(lambda row: "False" if row["user_search"] == product_name and row["daily"] == "True" else 
    ("True" if row["user_search"] == product_name and row["daily"] == "False" else row["daily"]), axis=1)

    df2["daily"] = df2.apply(lambda row: "False" if row["user_search"] == product_name and row["daily"] == "True" else 
    ("True" if row["user_search"] == product_name and row["daily"] == "False" else row["daily"]), axis=1)

    df.to_csv('cleaned_user_data.csv', index=False)
    df2.to_csv('scraped_data.csv', index=False)

    print(f"Toggled 'daily' for {product_name}.")

def delete(product_name):
    df = pd.read_csv('cleaned_user_data.csv', dtype=str)
    df2 = pd.read_csv('scraped_data.csv', dtype=str)
    df = df[df['user_search'] != product_name]
    df2 = df2[df2['user_search'] != product_name]
    df.to_csv('cleaned_user_data.csv', index=False)
    df2.to_csv('scraped_data.csv', index=False)
    print(f"deleted {product_name}.")



# import pandas as pd

# # Define your list of products and their original prices
# products = [
#     {"user_search": "ps5", "original_price": 700},
#     {"user_search": "iphone x", "original_price": 500},
#     {"user_search": "jordan 1", "original_price": 150},
#     {"user_search": "iphone 15 pro", "original_price": 800},
#     {"user_search": "airpods pro 2", "original_price": 250}
# ]

# # Load your existing cleaned user data CSV
# df = pd.read_csv("cleaned_user_data.csv")

# # Loop over products to add original price
# for product in products:
#     user_search_query = product["user_search"]
#     original_price = product["original_price"]
    
#     # Add original price as a new column for matching search queries
#     df.loc[df["user_search"].str.lower() == user_search_query.lower(), "original_price"] = original_price

# # Save the updated DataFrame to a new CSV
# df.to_csv("cleaned_user_data.csv", index=False)
# print("Original prices added to the CSV!")

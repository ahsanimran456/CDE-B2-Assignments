import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
# options.add_argument("--headless")  # Disable during debug
options.add_argument("--start-maximized")

CHROMEDRIVER_PATH = r"D:\downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

def extract_coin_data():
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    data = []
    for row in rows:
        try:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 9:
                price = cols[3].text if cols[3].text != "##### " else "N/A"
                volume = cols[7].text if cols[7].text != "##### " else "N/A"
                
                data.append({
                    'Name': cols[2].text.split('\n')[0],
                    'Symbol': cols[2].find_element(By.TAG_NAME, 'p').text,
                    'Price': price,
                    '24h %': cols[4].text,
                    '7d %': cols[5].text,
                    'Market Cap': cols[6].text,
                    'Volume (24h)': volume
                })
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return data

all_data = []
for page in range(1):
    driver.get(f"https://coinmarketcap.com/?page={page}")
    time.sleep(5)  # Let the page load completely

    for i in range(1, 120):  # Increase to scroll more rows
        try:
            row = driver.find_element(By.XPATH, f'//tbody/tr[{i}]')
            ActionChains(driver).move_to_element(row).perform()
            time.sleep(0.1)
        except:
            break

    # Give extra time for final elements
    time.sleep(3)

    page_data = extract_coin_data()
    all_data.extend(page_data)

driver.quit()

for coin in all_data:
    print(coin)

df = pd.DataFrame(all_data)
df.to_csv("top_100_coins.csv", index=False)
print(f"\n✅ Saved {len(df)} coins to 'top_100_coins.csv'")

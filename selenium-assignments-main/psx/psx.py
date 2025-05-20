import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # optional

CHROMEDRIVER_PATH = r"D:\downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

driver.get("https://www.psx.com.pk/market-summary/")

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".table-responsive table tbody tr"))
)

time.sleep(5)  

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

csv_filename = "psx_market_data.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    tables = soup.find_all("div", class_="table-responsive")

    for table_div in tables:
        try:
            table = table_div.find("table")
            if not table:
                continue

            sector_header = table.find("h4")
            sector_name = sector_header.get_text(strip=True) if sector_header else "UNKNOWN SECTOR"

            tbody = table.find("tbody")
            rows = tbody.find_all("tr")
            if len(rows) < 2:
                continue

            writer.writerow([f"=== {sector_name} ==="])

            headers = [td.get_text(strip=True) for td in rows[0].find_all("td")]
            writer.writerow(headers)

            for row in rows[1:]:
                cols = [td.get_text(strip=True) for td in row.find_all("td")]
                if len(cols) == len(headers):
                    writer.writerow(cols)

        except Exception as e:
            print(f"Error processing table: {e}")

print(f"✅ Sector-wise data saved to {csv_filename}")

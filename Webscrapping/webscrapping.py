import requests
from bs4 import BeautifulSoup
import openpyxl

# Excel workbook and sheet setup
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "Coin Data"
row_num = 1  # Start from first row

# Web scraping
url = 'https://coinmarketcap.com/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table', class_='sc-db1da501-3 ccGPRR cmc-table')

if table:
    rows = table.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        col_num = 1  # Start from first column in each row
        for td in tds:
            p_tag = td.find('p')
            # if p_tag:
            #     text = p_tag.get_text(strip=True)
            #     # Write to Excel
            #     sheet.cell(row=row_num, column=col_num).value = text
            #     col_num += 1
            print(p_tag)
        # if col_num > 1:
        #     row_num += 1  # Only increment row if data was added
else:
    print("Table not found")

# # Save Excel file
# wb.save("coin_data.xlsx")
# print("Data saved to coin_data.xlsx")

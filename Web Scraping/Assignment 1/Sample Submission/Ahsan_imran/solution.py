import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Prepare CSV file
with open('books_scraped.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Availability', 'Rating'])

    # Step 2: Loop through 50 pages
    for page in range(1, 51):
        url = f'http://books.toscrape.com/catalogue/page-{page}.html'
        response = requests.get(url)

        # Check if page exists
        if response.status_code != 200:
            print(f"⚠️ Page {page} not found!")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        # Step 3: Extract info from each book
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            availability = book.find('p', class_='instock availability').text.strip()
            rating_class = book.find('p')['class']
            rating = rating_class[1]

            # Step 4: Write to CSV
            writer.writerow([title, price, availability, rating])

        print(f"✅ Page {page} scraped.")

print("\n🎯 Done! All 50 pages scraped and saved to 'books_scraped.csv'.")

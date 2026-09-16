import requests
from bs4 import BeautifulSoup
import random
import pandas as pd


# Three categories we want to scrape
CATEGORIES = {
    "Fiction": "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html",
    "Mystery": "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "Nonfiction": "https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"
}


def get_book_links(category_url):
    """Get all book links from a category."""

    response = requests.get(category_url)

    if response.status_code != 200:
        print("Failed to access:", category_url)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for book in soup.select("article.product_pod h3 a"):
        link = book.get("href")

        if link:
            full_url = requests.compat.urljoin(category_url, link)
            links.append(full_url)

    return links


def scrape_book(url, category):
    """Scrape details of one book."""

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to scrape:", url)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        title = soup.find("h1").text.strip()

        price = soup.find(
            "p",
            class_="price_color"
        ).text.strip()

        rating = soup.find(
            "p",
            class_="star-rating"
        )["class"][1]

        availability = soup.find(
            "p",
            class_="instock availability"
        ).text.strip()

        return {
            "title": title,
            "price_gbp": price,
            "star_rating": rating,
            "availability": availability,
            "category": category
        }

    except AttributeError:
        print("Could not parse:", url)
        return None


# Store all scraped books
all_books = []
random.seed(42)

# Process each category
for category, category_url in CATEGORIES.items():

    print("\nCategory:", category)

    # Get all book links
    links = get_book_links(category_url)

    print("Books found:", len(links))

    # Randomly select 20 books
    selected_links = random.sample(links, 20)

    print("Randomly selected:", len(selected_links))

    # Scrape the selected books
    for link in selected_links:

        book = scrape_book(link, category)

        if book is not None:
            all_books.append(book)


# Convert to DataFrame
df = pd.DataFrame(all_books)


# Display results
print("\nTotal books scraped:", len(df))

print("\nBooks by category:")
print(df["category"].value_counts())

print("\nFirst 5 books:")
print(df.head())


# Save raw scraped data
df.to_csv(
    "data_pipeline/books_raw.csv",
    index=False
)

print("\nData saved to data_pipeline/books_raw.csv") 
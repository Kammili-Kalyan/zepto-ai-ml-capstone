# Data Pipeline

## Overview

This module scrapes book data from Books to Scrape, cleans the data, converts prices from GBP to INR, stores the data in SQLite, and performs SQL and Pandas analysis.

## Data Collection

- Source: Books to Scrape
- Categories scraped: 3
- Total books collected: 60
- Tools: Requests and BeautifulSoup

## Data Cleaning

The following fields were cleaned:

- `price_gbp` converted to float
- Star ratings converted from text to integers from 1 to 5
- Availability converted to boolean `in_stock`
- Category information retained for database relationships

## Currency Conversion

A fixed project conversion rate was used:

`1 GBP = 105.50 INR`

The rate is fixed as required by the project and is not fetched from a live API.

## Database

The cleaned data is stored in SQLite using related tables:

- `categories`
- `books`

The `books` table uses `category_id` as a foreign key to the `categories` table.

## SQL Analysis

The project includes SQL queries covering:

- Filtering with `WHERE`
- Sorting with `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `BETWEEN`
- Table `JOIN`

Query outputs are saved in the project for verification.

## Pandas Comparison

At least two SQL results are loaded using `pd.read_sql`.

The SQL JOIN result is reproduced using `pd.merge()` in Pandas and the outputs are compared.

## Files

- `scraper.py` — web scraping and cleaning
- `database.py` — SQLite database creation and insertion
- `queries.py` — SQL queries
- `queries.sql` — saved SQL queries
- `query_outputs.txt` — SQL query outputs
- `pandas_comparison.py` — SQL and Pandas comparison
- `pandas_comparison.txt` — comparison output
- `books.db` — SQLite database
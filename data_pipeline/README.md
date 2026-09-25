## Module 1 — Data Pipeline

### Overview

The Data Pipeline module implements an end-to-end data engineering workflow:

**Scraping → Cleaning → Currency Conversion → SQLite Storage → SQL Queries → Pandas Validation**

The data source is `books.toscrape.com`, a public website created for
scraping practice.

### Data Collection

The scraping pipeline uses:

- Python
- `requests`
- `BeautifulSoup`

Books are scraped from three different categories.

The final dataset contains 60 book records.

The following fields are collected:

- `title`
- `price`
- `star_rating`
- `availability`
- `category`

### Data Cleaning

The scraped fields are converted into appropriate data types.

# Price

The currency symbol is removed from the scraped price and the value is
converted into the numeric column:

`price_gbp`

# Rating

The text ratings are converted into integers:

- One → 1
- Two → 2
- Three → 3
- Four → 4
- Five → 5

The resulting column is:

`rating`

# Availability

The availability text is converted into a Boolean value in:

`in_stock`

This represents whether the book is currently available.

# Handling Parsing Problems

The pipeline includes handling for values that cannot be parsed correctly.
Numeric parsing problems are handled using the required median-imputation
approach, while rows that cannot be safely processed can be dropped rather
than allowing the pipeline to fail.

### Currency Conversion

The project-required fixed conversion rate is:

**1 GBP = 105.50 INR**

The `price_inr` column is calculated from `price_gbp` using this fixed
project-defined rate.

No external currency API is required.

### Database Design

The cleaned data is stored in SQLite using a normalized two-table schema.

The database contains:

- `categories`
- `books`

The `categories` table contains a primary key.

The `books` table contains a foreign key referencing the category.

This creates the required primary-key/foreign-key relationship and avoids
unnecessary duplication of category information.

### SQL Queries

At least five SQL queries are executed against the database.

The queries collectively demonstrate:

- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `IN` / `BETWEEN`
- `JOIN`

The SQL queries and their outputs are saved in the project.

### Pandas Validation

SQL query results are read into pandas DataFrames using:

`pd.read_sql()`

The JOIN result is also reproduced using:

`pd.merge()`

The SQL-based and pandas-based results are compared to verify that the
results match.

### How to Run

From the project root, run the Module 1 pipeline using the project's
data-pipeline script/notebook.

The pipeline performs the following steps:

1. Scrape the book data.
2. Clean the scraped fields.
3. Convert prices from GBP to INR using the fixed rate of 105.50.
4. Create/populate the SQLite database.
5. Execute the required SQL queries.
6. Generate/save the query outputs.
7. Perform the pandas `pd.read_sql()` and `pd.merge()` comparison.

### Design Decisions

1. `requests` and `BeautifulSoup` were selected for HTML scraping because
   the source website provides publicly accessible HTML data.
2. The fixed conversion rate of **1 GBP = 105.50 INR** is used because it
   is the project-defined baseline.
3. SQLite was selected because it provides a lightweight relational
   database suitable for this local project.
4. A normalized two-table schema was used to maintain the required
   primary-key/foreign-key relationship.
5. Pandas was used to independently reproduce the JOIN result and verify
   the SQL result.
import sqlite3
import pandas as pd

#read file
df=pd.read_csv("data_pipeline/books_cleaned.csv")
print("books loaded:",len(df))

#create data base
connection=sqlite3.connect("data_pipeline/books.db")
cursor=connection.cursor()

#create categories tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE                                     
     )"""
)

#create books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock BOOLEAN,
    category_id INTEGER,
    FOREIGN KEY(category_id)
        REFERENCES categories(category_id)
        )"""
)

cursor.execute("DELETE FROM books")
cursor.execute("DELETE FROM categories")

#insert data in categories
categories=df['category'].unique()

for category in categories:
    cursor.execute("""
        INSERT OR IGNORE INTO categories(category_name)
        VALUES (?)""",(category,)
        )
    
#insert data in books
for _,row in df.iterrows():
    cursor.execute("""
        INSERT INTO books
        (title,price_gbp,price_inr,rating,in_stock,category_id)
        VALUES(?,?,?,?,?,
            (SELECT category_id
            FROM categories
            WHERE category_name=?
            )
        )
        """,
        (
            row['title'],
            row['price_gbp'],
            row['price_inr'],
            row['rating'],
            row['in_stock'],
            row['category']
        )
    )

#save changes
connection.commit()

#check no of records
cursor.execute("SELECT COUNT(*) FROM books")
book_count=cursor.fetchone()[0]
print("Books inserted:",book_count)

cursor.execute("SELECT COUNT(*) FROM categories")
category_count=cursor.fetchone()[0]
print("Categories inserted:",category_count)

#close data base
connection.close()
print("Database created successfully")
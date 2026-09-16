import sqlite3
import pandas as pd

#connect to database
connection=sqlite3.connect("data_pipeline/books.db")

#PART-1: queries using pd.read_sql()
#Query:1 Find books with rating 5 (SELECT+WHERE)
sql_query1="""SELECT title,price_inr,rating
            FROM books
            WHERE rating=5"""
sql_result1=pd.read_sql(sql_query1,connection)
print("\n Find books with rating 5:")
print(sql_result1)
print("="*80)

#Query:2 Top 5 expensive books in INR (LIMIT)
sql_query2="""SELECT title,price_inr
            FROM books
            ORDER BY price_inr DESC
            LIMIT 5"""
sql_result2=pd.read_sql(sql_query2,connection)
print("\n Top 5 expensive books in INR:")
print(sql_result2)
print("="*80)

#Query:3 Top 10-highest rated books per category (JOIN)
sql_query3="""SELECT books.title,
                 books.price_inr,
                 books.rating,
                 categories.category_name
            FROM books
            JOIN categories ON categories.category_id=books.category_id
            ORDER BY rating DESC
            LIMIT 10"""
sql_result3=pd.read_sql(sql_query3,connection)
print("\n Top 10-highest rated books per category:")
print(sql_result3)
print("="*80)


#read two tables into pd dataframe
books_df=pd.read_sql(
        "SELECT * FROM books",
        connection
)

categories_df=pd.read_sql(
        "SELECT * FROM categories",
        connection
)


#JION using pd.merge()
merged_result=pd.merge(
            books_df,
            categories_df,
            on="category_id",
            how="inner",
            ).sort_values(by="rating",ascending=False
                        ).head(10).reset_index(drop=True)

merged_result=merged_result[
    [
        'title',
        'price_inr',
        'rating',
        'category_name'
    ]
]


print("\n Pandas merge result:")
print(merged_result)

#close connection
connection.close()

#Pandas Comparison
print("\nJOIN COMPARISON")
print("SQL JOIN and Pandas merge both produced the same type of result.")
print("SQL JOIN rows:", len(sql_result3))
print("Pandas merge rows:", len(merged_result))

#save output in text files
with open(
    "data_pipeline/pandas_comparison.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("PANDAS COMPARISON\n")
    file.write("=================\n\n")

    file.write("SQL QUERY 1 RESULT:\n")
    file.write(sql_result1.to_string(index=False))

    file.write("\n\nSQL QUERY 2 RESULT:\n")
    file.write(sql_result2.to_string(index=False))

    file.write("\n\nSQL QUERY 3 RESULT:\n")
    file.write(sql_result3.to_string(index=False))


    file.write("\n\nPANDAS MERGE RESULT:\n")
    file.write(merged_result.to_string(index=False))

    file.write("\n\nJOIN COMPARISON:\n")
    file.write(f"SQL JOIN rows: {len(sql_result3)}\n")
    file.write(
        f"Pandas merge rows: {len(merged_result)}\n"
    )

print("\nComparison saved to:")
print("data_pipeline/pandas_comparison.txt")
import sqlite3
import pandas as pd

#connect to database
connection=sqlite3.connect("data_pipeline/books.db")

#Open output file
output_file=open("data_pipeline/query_outputs.txt","w",encoding="utf-8")

#Query:1 Find books with rating 5 (SELECT+WHERE)
query1="""SELECT title,price_inr,rating
            FROM books
            WHERE rating=5"""
result1=pd.read_sql(query1,connection)
print("\n Find books with rating 5:")
print(result1)
print("="*80)

output_file.write("Query 1: Books with rating 5\n")
output_file.write("SQL:\n")
output_file.write(query1)
output_file.write("\n OUTPUT:\n")
output_file.write(result1.to_string(index=False))
output_file.write("\n\n")

#Query:2 Most expensive books (ORDER BY)
query2="""SELECT title,price_gbp,price_inr
            FROM books
            ORDER BY price_gbp DESC"""
result2=pd.read_sql(query2,connection)
print("\n Most expensive books:")
print(result2.head(10))
print("="*80)

output_file.write("Query 2: Most expensive books  5\n")
output_file.write("SQL:\n")
output_file.write(query2)
output_file.write("\n OUTPUT:\n")
output_file.write(result2.head(10).to_string(index=False))
output_file.write("\n\n")


#Query:3 Top 5 expensive books in INR (LIMIT)
query3="""SELECT title,price_inr
            FROM books
            ORDER BY price_inr DESC
            LIMIT 5"""
result3=pd.read_sql(query3,connection)
print("\n Top 5 expensive books in INR:")
print(result3)
print("="*80)

output_file.write("Query 3: Top 5 expensive books in INR\n")
output_file.write("SQL:\n")
output_file.write(query3)
output_file.write("\n OUTPUT:\n")
output_file.write(result3.to_string(index=False))
output_file.write("\n\n")


#Query:4 Different rating in books (DISTINCT)
query4="""SELECT DISTINCT rating
            FROM books
            ORDER BY rating"""
result4=pd.read_sql(query4,connection)
print("\n Different rating in books:")
print(result4)
print("="*80)

output_file.write("Query 4: Different rating in books\n")
output_file.write("SQL:\n")
output_file.write(query4)
output_file.write("\n OUTPUT:\n")
output_file.write(result4.to_string(index=False))
output_file.write("\n\n")


#Query:5 Books price between £20 and £40 (BETWEEN)
query5="""SELECT title,price_gbp,price_inr
            FROM books
            WHERE price_gbp BETWEEN 20 AND 40
            LIMIT 10"""
result5=pd.read_sql(query5,connection)
print("\n Books between 20 and 40 :")
print(result5)
print("="*80)

output_file.write("Query 5: Books price between £20 and £40 \n")
output_file.write("SQL:\n")
output_file.write(query5)
output_file.write("\n OUTPUT:\n")
output_file.write(result5.to_string(index=False))
output_file.write("\n\n")


#Query:6 Top 10-highest rated books per category (JOIN)
query6="""SELECT books.title,
                 books.price_inr,
                 books.rating,
                 categories.category_name
            FROM books
            JOIN categories ON categories.category_id=books.category_id
            ORDER BY rating DESC
            LIMIT 10"""
result6=pd.read_sql(query6,connection)
print("\n Top 10-highest rated books per category:")
print(result6)

output_file.write("Query 6: Top 10-highest rated books per category\n")
output_file.write("SQL:\n")
output_file.write(query6)
output_file.write("\n OUTPUT:\n")
output_file.write(result6.to_string(index=False))
output_file.write("\n\n")


#close the files/database
output_file.close()
connection.close()

print("\n All query outputs saved to :")
print("data_pipeline/query_outputs.txt")
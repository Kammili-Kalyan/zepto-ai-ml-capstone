# Query:1 SELECT+WHERE
SELECT title,price_inr,rating
FROM books
WHERE rating=5;

#Query:2 ORDER BY
SELECT title,price_gbp,price_inr
FROM books
ORDER BY price_gbp DESC;

#Query:3 LIMIT
SELECT title,price_inr
FROM books
ORDER BY price_inr DESC
LIMIT 5;

#Query:4 DISTINCT
SELECT DISTINCT rating
FROM books
ORDER BY rating;

#Query:5 BETWEEN
SELECT title,price_gbp,price_inr
FROM books
WHERE price_gbp BETWEEN 20 AND 40
LIMIT 10;

#Query:6 JOIN
SELECT books.title,
        books.price_inr,
        books.rating,
        categories.category_id
FROM books
JOIN categories 
    ON categories.category_id=books.category_id
ORDER BY rating DESC
LIMIT 10;
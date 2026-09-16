import pandas as pd

#import data set as df
df=pd.read_csv("data_pipeline/books_raw.csv")

print("\n Raw data:")
print(df.head())
print("\n Data types:")
print(df.dtypes)

#convert price into float
df['price_gbp']=df['price_gbp'].str.replace("Â£","",regex=False).astype(float)

#convert rating text into numeric
mapping={
    "One":1,
    "Two":2,
    "Three":3,
    "Four":4,
    "Five":5
}
df['rating']=df['star_rating'].map(mapping)

#Convert availability into boolean(true/false)
df["in_stock"] = (
    df["availability"]
    .fillna("")
    .str.strip()
    .str.lower()
    .str.startswith("in stock")
)
#convert gbp into inr
GBP_TO_INR=105.50
df['price_inr']=(df['price_gbp']*GBP_TO_INR).round(2)

#removing unneccessary raw columns
df=df[['title','price_gbp','price_inr','rating','in_stock','category']]

#checking missing values
print("\n missing values:")
print(df.isnull().sum())

#Display cleaned data
print("\n Cleaned data:")
print(df.head())

print("\n Data types after cleaning:")
print(df.dtypes)

print("\n Number of books:",len(df))

#saved cleaned data
df.to_csv("data_pipeline/books_cleaned.csv",index=False)
print("\n Cleaned data saved successfully")
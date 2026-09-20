import pymongo
import os
import csv

# Connect to MongoDB
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["VideoGames"]

#Import the CSV
raw_collection = db["VideoGamesSales"]
raw_collection.drop()

with open("VideoGameSales.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw_collection.insert_one(dict(row))

print(f"Imported {raw_collection.count_documents({})} raw records")

# Data processing
tuples = []

for doc in raw_collection.find():
    genre = doc.get("Genre", "").strip()
    platform = doc.get("Platform", "").strip()
    publisher  = doc.get("Publisher", "").strip()
    year       = doc.get("Year", "").strip()
    global_sales = doc.get("Global_Sales", "").strip()

    if not genre or genre in ["N/A", "Unknown"]:
        continue
    if not platform or platform in ["N/A", "Unknown"]:
        continue
    if not publisher or publisher in ["N/A", "Unknown"]:
        continue
    if not year or year in ["N/A", "Unknown"]:
        continue
    try:
        year = int(float(year))         
        global_sales = float(global_sales)  
    except (ValueError, TypeError):
        continue 
    tuples.append((genre, platform, publisher, global_sales, year))

with open("task1_1_output.txt", "w", encoding = "utf-8") as f:
    for t in tuples:
        genre, platform, publisher, global_sales, year = t 
        line = f"{genre}\t{platform}\t{publisher}\t{global_sales}\t{year}\n"
        f.write(line)

# Insert the tuples into game_extracted collection
extracted_collection = db["game_extracted"]
extracted_collection.drop()

docs_to_insert = []
for t in tuples:
    genre, platform, publisher, global_sales, year = t
    docs_to_insert.append({
        "Genre": genre, 
        "Platform": platform,
        "Publisher":publisher,
        "Global_sales": global_sales, 
        "Year": year
    })

extracted_collection.insert_many(docs_to_insert)
print(f"Inserted {len(docs_to_insert)} records into game_extraced")

# Check the output
with open("task1_1_output.txt", "r") as f:
    lines = f.readlines()
    print(f"Lines in txt file: {len(lines)}")
    print("First 3 lines:")
    for line in lines[:3]:
        print(line)
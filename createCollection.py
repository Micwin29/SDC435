#Michael Winstead
#SDC435 2.3 GP
#6 26, 2026

import json

import pymongo

# *** CREATE SECTION***
#Notify when script is starting
print("Connecting to local Mongo database...")

#Connect to the local Mongo database
myClient = pymongo.MongoClient("mongodb://localhost:27017/")

#Create a new database
db = myClient["SampleDatabase"]

#Create a new collection in the database
myCollection = db["ReviewInfo"]

#Import the JSON data into the collection
print("Importing data from file...")
for line in open('dataset_en_dev.json', 'r'):dataSet = json.loads(line)
myCollection.insert_one(dataSet)
print("Data imported successfully!")
#Display status of database
print("List of available databases: ")
print(myClient.list_database_names())
print("List of available collections in this database: ")
print(db.list_collection_names())

# *** READ SECTION ***
#Display a document
print("A sample document contains: ")
sampleData = myCollection.find_one()
print(sampleData)

#Filter down to one field and display several documents
print("\nFive sample review titles are: ")
query = myCollection.find({}, {"_id": 0, "review_title":
1}).limit(5)
for titles in query:
    print(titles)

#Filter for only 4 and 5 star reviews and limit to 3 results
print("\nThree sample 4+ star reviews are: ")
query = {"stars": {"$gte": "4"}}
showFields = {"_id": False, "review_body": True, "stars":
True}
data = myCollection.find(query, showFields).limit(3)

for doc in data:
    print(doc)
    print()

#Filter for a word in the review_title, limit results
print("\nTwo sample reviews with the word Awesome: ")
query = {"review_title": {"$regex": "/*Awesome/*"}}
showFields = {"_id": False, "review_title": True,
"review_body": True}
data = myCollection.find(query, showFields).limit(2)

for doc in data:
    print(doc)
    print()

# *** UPDATE SECTION ***
#Insert a new document into the collection
newData = {"reviewer_id": "Test", "review_title": "Title",
"stars": "0"}
insertQuery = myCollection.insert_one(newData)
print("New document inserted.")

#Update a document in the collection
query = {"reviewer_id": "Test"}
updateData = {"$set": {"reviewer_id": "UpdateTest", "stars":
"-1"}}
myCollection.update_one(query, updateData)
print("New document has been updated to: ")
print(myCollection.find_one({"reviewer_id": "UpdateTest"}))

# *** DELETE SECTION ***
#Delete a single document from the collection
print("Number of documents before: ")
print(myCollection.count_documents({}))
query = {"stars": "-1"}
myCollection.delete_one(query)
print("Number of documents after removing a -1 star review:")
print(myCollection.count_documents({}))

#Delete multiple documents from the collection
query = {"product_category": "shoes"}
shoes = myCollection.delete_many(query)

print("Removed all documents under the shoes product category.")
print("Number of documents deleted: " +
str(shoes.deleted_count))

#Delete all documents from the collection
print("Removing all documents from the collection...")
removeData = myCollection.delete_many({})

print("Number of documents deleted: " +
str(removeData.deleted_count))

#Delete a collection
myCollection.drop()

print("Collection removed!")

#Display end of program message
print("Program has ended!")

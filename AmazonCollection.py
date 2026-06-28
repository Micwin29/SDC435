#Michael Winstead
#SDC435 2.5PA
#6 28, 2026

import json

import pymongo

# ***Create Section***
#Notify when script is Starting
print("Connecting to local Mongo database...")
# Connect to Amazon MongoDB
myClient= pymongo.MongoClient("mongodb://localhost:27017/")
#DataBase
db = myClient["AmazonReviews"]
#Collection
myCollection = db["ReviewData"]

#Import the JSON data into the collection
print("Importing data from file...")
for line in open('dataset_en_dev.json', 'r'):
    dataSet = json.loads(line)
    myCollection.insert_one(dataSet)

print("Data imported successfully!")

#Display status of database
print("List of available databases: ")
print(myClient.list_database_names())
print("List of available collections in this database: ")
print(db.list_collection_names())

#***Read Section***
#New review document
def create_document():
    print("\nCreate New Review")

    document = {
        "review_id": input("Review ID: "),
        "product_id": input("Product ID: "),
        "reviewer_id": input("Reviewer ID: "),
        "stars": int(input("Stars (1-5): ")),
        "review_body": input("Review Body: "),
        "review_title": input("Review Title: "),
        "language": input("Language: "),
        "product_category": input("Product Category: ")
    }

    collection.insert_one(document)
    print("Document added successfully.\n")

#Retrieve one document using find_one()
def find_one_document():
    review_id = input("Enter Review ID: ")

    result = collection.find_one({"review_id": review_id})

    if result:
        print("\nDocument Found")
        print(result)
    else:
        print("No document found.")

#Retrieve multiple documents using advanced queries
def advanced_search():

    while True:

        print("\nAdvanced Search")
        print("1. Stars >= value")
        print("2. Stars < value")
        print("3. Search Review Title")
        print("4. Search Review Body")
        print("5. Return to Main Menu")

        choice = input("Choice: ")

        if choice == "1":

            stars = int(input("Minimum stars: "))

            results = collection.find({"stars": {"$gte": stars}})

            print()

            for doc in results:
                print(doc)

        elif choice == "2":

            stars = int(input("Maximum stars: "))

            results = collection.find({"stars": {"$lt": stars}})

            print()

            for doc in results:
                print(doc)

        elif choice == "3":

            word = input("Word in review title: ")

            results = collection.find(
                {"review_title":
                     {"$regex": word, "$options": "i"}}
            )

            print()

            for doc in results:
                print(doc)

        elif choice == "4":

            word = input("Word in review body: ")

            results = collection.find(
                {"review_body":
                     {"$regex": word, "$options": "i"}}
            )

            print()

            for doc in results:
                print(doc)

        elif choice == "5":
            break

        else:
            print("Invalid selection.")



# **** Update ***
#Update
def update_document():

    review_id = input("Enter Review ID to update: ")

    field = input(
        "Field to update "
        "(review_id, product_id, reviewer_id, stars, "
        "review_body, review_title, language, "
        "product_category): "
    )

    new_value = input("New value: ")

    if field == "stars":
        new_value = int(new_value)

    result = collection.update_one(
        {"review_id": review_id},
        {"$set": {field: new_value}}
    )

    if result.modified_count > 0:
        print("Document updated.")
    else:
        print("No matching document found.")


#***Delete Section****
# Delete one document
def delete_document():

    review_id = input("Enter Review ID to delete: ")

    result = collection.delete_one({"review_id": review_id})

    if result.deleted_count > 0:
        print("Document deleted.")
    else:
        print("Document not found.")
        
#Delete all documents
def delete_all_documents():

    confirm = input(
        "Delete ALL documents? (yes/no): "
    )

    if confirm.lower() == "yes":
        result = collection.delete_many({})
        print(result.deleted_count,
              "documents removed.")
    else:
        print("Operation cancelled.")

#Delete colletion 
def delete_collection():

    confirm = input(
        "Delete the ReviewData collection? (yes/no): "
    )

    if confirm.lower() == "yes":
        collection.drop()
        print("Collection deleted.")
    else:
        print("Operation cancelled.")


#*** Main Menu Section***
# Main Menu
def menu():

    while True:

        print("\n========== MongoDB CRUD Menu ==========")
        print("1. Query for document")
        print("2. Add a new document")
        print("3. Search a document")
        print("4. Update fields of a document")
        print("5. Delete a document")
        print("6. Delete all document from the collection")
        print("7. Delete a collection")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            find_one_document()

        elif choice == "2":
            create_document()

        elif choice == "3":
            advanced_search()

        elif choice == "4":
            update_document()

        elif choice == "5":
            delete_document()

        elif choice == "6":
            delete_all_documents()

        elif choice == "7":
            delete_collection()

        elif choice == "8":
            print("Goodbye!")
            client.close()
            break

        else:
            print("Invalid choice.")



# Program Entry Point
if __name__ == "__main__":
    menu()

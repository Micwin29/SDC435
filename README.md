# SDC435
#Michael Winstead
#Date: June 2026
#1.8 PA

import json

import redis

# Connect to Redis database
r = redis.Redis(host='localhost', port=6379, db=0)


# Create a new set
def create_set():
    key = input("\nEnter the key you wish to add: ")

    num_members = int(input("Enter how many members this set will have: "))

    for i in range(num_members):
        member = input("\nEnter the next member value: ")
        r.sadd(key, member)

    print(f"\nSet '{key}' created successfully.")


# Retrieve members from a set
def read_set():
    key = input("\nEnter the key to retrieve: ")

    if r.exists(key):
        members = r.smembers(key)

        print("\nSet Members:")
        for member in members:
            print(member.decode('utf-8'))
    else:
        print("\nSet not found.")


# Update members of a set
def update_set():
    key = input("\nEnter the key of the set you wish to update: ")

    if not r.exists(key):
        print("\nSet does not exist.")
        return

    while True:
        print("\nPlease type in a number and press enter to execute the menu option.")
        print("1. Add new member")
        print("2. Remove member")
        print("3. Remove all members")
        print("4. Exit Update Menu")

        choice = input()

        if choice == "1":
            member = input("\nEnter member to add: ")
            r.sadd(key, member)
            print("Member added.")

        elif choice == "2":
            member = input("\nEnter member to remove: ")
            r.srem(key, member)
            print("Member removed.")

        elif choice == "3":
            members = r.smembers(key)

            print("\nRemoving all set members...")

            for member in members:
                print(f"Removing Member: {member}...")
                r.srem(key, member)

            print("\nThe cardinality of the set is now:")
            print(r.scard(key))

        elif choice == "4":
            break

        else:
            print("Invalid option.")


# Delete a specific set
def delete_set():
    key = input("\nEnter the key you wish to delete: ")

    if r.delete(key):
        print(f"\nSet '{key}' deleted successfully.")
    else:
        print("\nSet not found.")


# Delete all data in database
def delete_all():
    confirm = input(
        "\nAre you sure you want to delete ALL data? (yes/no): "
    )

    if confirm.lower() == "yes":
        r.flushdb()
        print("\nAll data deleted from database.")
    else:
        print("\nOperation cancelled.")


# Main menu
def main():
    while True:
        print("\nType in a number and press enter to execute the menu option.")
        print("1. Query for set members")
        print("2. Add a new set")
        print("3. Update members of a set")
        print("4. Delete a set")
        print("5. Delete all data from the database")
        print("6. Exit the program")

        choice = input()

        if choice == "1":
            read_set()

        elif choice == "2":
            create_set()

        elif choice == "3":
            update_set()

        elif choice == "4":
            delete_set()

        elif choice == "5":
            delete_all()

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Please try again.")


# Start the program
if __name__ == "__main__":
    main()


import json
import os

from product import Product
from inventory import Inventory

FILENAME = "inventory.json"
DATA_DIR = os.environ.get("DATA_DIR", ".")
FILEPATH = os.path.join(DATA_DIR, FILENAME)
LINE = "-" * 49


def load_inventory():
    if os.path.exists(FILEPATH):
        print(f"{FILENAME} found.")
        try:
            with open(FILEPATH, "r") as f:
                inventory = Inventory.from_dict(json.load(f))
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError, KeyError, TypeError,
                AttributeError, ValueError):
            print("Could not read file. Starting with an empty inventory.")
    else:
        print(f"{FILENAME} not found. Starting with an empty inventory.")
    return Inventory()


def save_inventory(inventory):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FILEPATH, "w") as f:
        json.dump(inventory.to_dict(), f, indent=4)


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Remove Product")
    print("7. Exit")
    print("-----------------------------")


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if inventory.search_product(product_id):
        print("\nA product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        product = Product(product_id, name, price, stock)
    except ValueError as e:
        print(f"\nInvalid input. Product not added. ({e})")
        return
    if not inventory.add_product(product):
        print("\nA product with that ID already exists.")
        return
    print("\nProduct added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    try:
        new_stock = int(input("\nNew Stock Quantity: "))
        inventory.update_stock(product.product_id, new_stock)
    except ValueError as e:
        print(f"\nInvalid input. Stock not updated. ({e})")
        return
    print("\nStock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print(LINE)


def remove_product(inventory):
    print("\nRemove Product")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    confirm = input("\nAre you sure you want to remove this product? (y/n): ")
    if confirm.strip().lower() != "y":
        print("\nRemoval cancelled.")
        return
    inventory.remove_product(product.product_id)
    print("\nProduct removed successfully!")


def main():
    print("=" * 41)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 41)
    print()
    inventory = load_inventory()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {FILENAME}.")
        elif choice == "6":
            remove_product(inventory)
        elif choice == "7":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
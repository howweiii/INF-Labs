import json
import os

FILENAME = "inventory.json"
LINE = "-" * 49

# Inventory dictionary: a list of product dictionaries + a history of
# every transaction amount (not just a running total).
inventory = {"products": [], "transactions": []}


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


def find_product(product_id):
    for product in inventory["products"]:
        if product["id"].upper() == product_id.upper():
            return product
    return None


def display_all():
    print("\nCurrent Inventory")
    print(LINE)
    for p in inventory["products"]:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print(LINE)


def add_product():
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if find_product(product_id):
        print("\nA product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("\nInvalid number entered. Product not added.")
        return

    inventory["products"].append(
        {"id": product_id, "name": name, "price": price, "stock": stock}
    )
    # Record the value of the stock added as a transaction
    inventory["transactions"].append(
        {"product_id": product_id, "type": "add", "amount": round(price * stock, 2)}
    )
    print("\nProduct added successfully!")


def update_stock():
    print("\nUpdate Stock")
    product = find_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    try:
        new_stock = int(input("\nNew Stock Quantity: "))
    except ValueError:
        print("\nInvalid number entered. Stock not updated.")
        return

    change = new_stock - product["stock"]
    inventory["transactions"].append(
        {"product_id": product["id"], "type": "update",
         "amount": round(change * product["price"], 2)}
    )
    product["stock"] = new_stock
    print("\nStock updated successfully!")


def search_product():
    print("\nSearch Product")
    product = find_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(LINE)


def remove_product():
    print("\nRemove Product")
    product = find_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    confirm = input("\nAre you sure you want to remove this product? (y/n): ")
    if confirm.strip().lower() != "y":
        print("\nRemoval cancelled.")
        return

    inventory["products"].remove(product)
    # Record the value of the stock removed as a negative transaction
    inventory["transactions"].append(
        {"product_id": product["id"], "type": "remove",
         "amount": round(-product["price"] * product["stock"], 2)}
    )
    print("\nProduct removed successfully!")


def load_inventory():
    global inventory
    if os.path.exists(FILENAME):
        print(f"{FILENAME} found.")
        try:
            with open(FILENAME, "r") as f:
                inventory = json.load(f)
            inventory.setdefault("products", [])
            inventory.setdefault("transactions", [])
            print("Inventory loaded successfully.")
        except (json.JSONDecodeError, OSError):
            print("Could not read file. Starting with an empty inventory.")
            inventory = {"products": [], "transactions": []}
    else:
        print(f"{FILENAME} not found. Starting with an empty inventory.")
        inventory = {"products": [], "transactions": []}


def save_inventory():
    with open(FILENAME, "w") as f:
        json.dump(inventory, f, indent=4)


def main():
    print("=" * 41)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 41)
    print()
    load_inventory()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()
        if choice == "1":
            display_all()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            search_product()
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory()
            print(f"Inventory saved successfully to {FILENAME}.")
        elif choice == "6":
            remove_product()
        elif choice == "7":
            print("\nSaving inventory before exit...")
            save_inventory()
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
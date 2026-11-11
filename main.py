import json
import os

from product import PhysicalProduct, DigitalProduct, Product, CanBeShipped
from supplier import Supplier
from inventory import Inventory
from order import Order

FILENAME: str = "inventory.json"
DATA_DIR: str = os.environ.get("DATA_DIR", ".")
FILEPATH: str = os.path.join(DATA_DIR, FILENAME)
LINE: str = "-" * 49


def load_inventory() -> Inventory:
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


def save_inventory(inventory: Inventory) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FILEPATH, "w") as f:
        json.dump(inventory.to_dict(), f, indent=4)


def print_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Remove Product")
    print("7. Assign Supplier to Product")
    print("8. Show Supplier Details")
    print("9. Create Order")
    print("10. Exit")
    print("-----------------------------")


def get_supplier(inventory: Inventory) -> Supplier:
    """Reuse an existing supplier by ID, or create a new independent one."""
    supplier_id = input("Supplier ID: ").strip()
    supplier = inventory.find_supplier(supplier_id)
    if supplier:
        print(f"Using existing supplier: {supplier}")
        return supplier
    name = input("Supplier Name: ").strip()
    email = input("Supplier Contact Email: ").strip()
    return Supplier(supplier_id, name, email)


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if inventory.find_product(product_id):
        print("\nA product with that ID already exists.")
        return

    print("\nProduct Type")
    print("1. Physical")
    print("2. Digital")
    product_type = input("Choose type (1/2): ").strip()
    if product_type not in ("1", "2"):
        print("\nInvalid product type. Product not added.")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        supplier = get_supplier(inventory)
        product: Product
        if product_type == "1":
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(product_id, name, price, stock,
                                      supplier, weight)
        else:
            size = float(input("Download Size (MB): "))
            product = DigitalProduct(product_id, name, price, stock,
                                     supplier, size)
    except ValueError as e:
        print(f"\nInvalid input. Product not added. ({e})")
        return
    if not inventory.add_product(product):
        print("\nA product with that ID already exists.")
        return
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: ").strip())
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


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("\nSupplier Details")
    product.supplier.display_information()
    print(LINE)


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    product = inventory.find_product(input("Enter Product ID: ").strip())
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


def assign_supplier(inventory: Inventory) -> None:
    print("\nAssign Supplier to Product")
    product = inventory.find_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Supplier: {product.supplier}")
    try:
        supplier = get_supplier(inventory)
    except ValueError as e:
        print(f"\nInvalid input. Supplier not changed. ({e})")
        return
    inventory.assign_supplier(product.product_id, supplier)
    print("\nSupplier assigned successfully!")


def show_supplier_details(inventory: Inventory) -> None:
    print("\nSupplier Details")
    suppliers = inventory.get_suppliers()
    if not suppliers:
        print("\nNo suppliers found.")
        return

    print("\nAvailable Suppliers")
    print(LINE)
    for supplier in suppliers:
        print(supplier)
    print(LINE)

    supplier_id = input("\nEnter Supplier ID: ").strip()
    found = inventory.find_supplier(supplier_id)
    if not found:
        print("\nSupplier not found.")
        return

    print("\nSupplier Found")
    print(LINE)
    found.display_information()
    print("\nProducts supplied:")
    for product in inventory.get_products_by_supplier(found.supplier_id):
        print(f"  - {product.product_id}: {product.name}")
    print(LINE)


def create_order(inventory: Inventory) -> None:
    """Build an Order. The Order creates its own OrderLines; this function
    only hands it a Product (found in the inventory) and a quantity."""
    print("\nCreate Order")
    try:
        order = Order(input("Order ID: ").strip())
    except ValueError as e:
        print(f"\nInvalid input. Order not created. ({e})")
        return

    print("\nAdd products to the order. Leave Product ID blank to finish.")
    while True:
        product_id = input("\nProduct ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if not product:
            print("Product not found.")
            continue
        try:
            quantity = int(input(f"Quantity of {product.name}: "))
            order.add_order_line(product, quantity)
        except ValueError as e:
            print(f"Invalid input. Line not added. ({e})")
            continue
        print("Order line added.")

    if not order.order_lines:
        print("\nNo order lines added. Order discarded.")
        return

    print("\nOrder Summary")
    print(LINE)
    order.display_information()
    print(LINE)


def main() -> None:
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
            assign_supplier(inventory)
        elif choice == "8":
            show_supplier_details(inventory)
        elif choice == "9":
            create_order(inventory)
        elif choice == "10":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 10.")


if __name__ == "__main__":
    main()
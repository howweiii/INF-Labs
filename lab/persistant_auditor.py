TAX_RATE = 0.10
INVENTORY_FILE = "inventory.txt"


def load_inventory():
    """Reads the total (line 1) and orders (other lines) from the file."""
    total = 0
    orders = []
    try:
        with open(INVENTORY_FILE, "r") as file:
            lines = file.read().splitlines()
        total = int(lines[0])
        for line in lines[1:]:
            order_id, name, quantity = line.split(",")
            orders.append((int(order_id), name, int(quantity)))
    except (FileNotFoundError, ValueError, IndexError):
        return 0, []
    return total, orders


def save_inventory(total, orders):
    """Writes the total on line 1, then one 'id,name,quantity' line per order."""
    with open(INVENTORY_FILE, "w") as file:
        file.write(f"{total}\n")
        for order_id, name, quantity in orders:
            file.write(f"{order_id},{name},{quantity}\n")


def display_orders(orders):
    """Shows the saved orders."""
    print("Current Orders:")
    if not orders:
        print("(No previous orders found)")
    for order_id, name, quantity in orders:
        print(f"{order_id}, {name}, {quantity}")
    print("-" * 47)


def get_quantity():
    """Asks for a quantity. Returns a whole number >= 0, or None if invalid."""
    entry = input("Enter Quantity: ").strip()
    if not entry.isdigit():
        print("Invalid input. Please enter a positive whole number.")
        return None
    return int(entry)


def process_delivery(total, quantity):
    """Returns the new inventory total."""
    return total + quantity


def calculate_tax(quantity):
    """Returns 10% tax for this order."""
    return quantity * TAX_RATE


def generate_report(transactions, units, failed):
    """Prints the audit report for this session."""
    print("\n***Audit Report***")
    print("Total Transactions Recorded:", transactions)
    print("Total Units Processed:", units)
    print("Number of Failed/Rejected Entries:", failed)


# Main program
inventory, orders = load_inventory()
transactions = 0
units = 0
failed = 0

display_orders(orders)

while True:
    name = input("Enter Product Name or Quit to exit: ").strip()

    if name.lower() == "quit":
        break

    if name == "" or "," in name:
        print("Product name cannot be empty or contain commas.")
        failed += 1
        continue

    quantity = get_quantity()
    if quantity is None:
        failed += 1
        continue

    order_id = 1001 + len(orders)
    inventory = process_delivery(inventory, quantity)
    tax = calculate_tax(quantity)
    orders.append((order_id, name, quantity))
    transactions += 1
    units += quantity

    print("\nNew Order Added:")
    print(f"{order_id}, {name}, {quantity}")
    print(f"Tax : ${tax:.2f}")
    print(f"Total Inventory: {inventory}\n")

    if inventory > 500:
        print("Inventory limit exceeded!")
        break

save_inventory(inventory, orders)
print(f"Order successfully saved to {INVENTORY_FILE}")

generate_report(transactions, units, failed)
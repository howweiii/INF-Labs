TAX_RATE = 0.10


def get_valid_input():
    """Prompts for input and returns a valid integer, None (for invalid), or 'quit'."""
    entry = input("Enter stock quantity (or 'quit' to stop): ").strip()

    if entry.lower() == "quit":
        return "quit"

    if not entry.lstrip("-").isdigit():
        print("Invalid input. Please enter a number.")
        return None

    quantity = int(entry)

    if quantity < 0:
        print("Negative numbers not allowed.")
        return None

    return quantity


def process_delivery(current_total, new_value):
    """Calculates and returns the new inventory total."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates tax (10%) for a specific delivery amount."""
    return amount * TAX_RATE


def generate_report(total_units, failed_attempts, successful_deliveries, total_tax):
    """Prints the final summary report."""
    print("\n--- Final Report ---")
    print("Total Deliveries Processed:", successful_deliveries)
    print("Number of Failed/Rejected Entries:", failed_attempts)
    print("Final Inventory Total:", total_units)
    print(f"Total Tax Collected: {total_tax:.2f}")


# Main execution flow
inventory = 0
failed_entries = 0
successful_deliveries = 0
total_tax = 0

while True:
    input_value = get_valid_input()

    if input_value == "quit":
        break

    if input_value is None:
        failed_entries += 1
        continue

    # Process valid entry
    quantity = input_value
    inventory = process_delivery(inventory, quantity)
    tax = calculate_tax(quantity)
    total_tax += tax
    successful_deliveries += 1

    print(f"Current inventory: {inventory}")
    print(f"Tax for this delivery: {tax:.2f}")
    print(f"Total Tax: {total_tax:.2f}")

    if inventory > 500:
        print("Inventory limit exceeded!")
        break

generate_report(inventory, failed_entries, successful_deliveries, total_tax)
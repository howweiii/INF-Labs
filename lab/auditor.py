#Initialize inventory to zero
inventory = 0
failed_entries = 0

while True:
    entry = input("Enter stock quantity (or 'quit' to stop): ")
    
    if entry == "quit":
        print("Total Units Processed:", inventory)
        print("Number of Failed/Rejected Entries:", failed_entries)
        break
    
    if not entry.lstrip("-").isdigit():
        print("Invalid input. Please enter a number.")
        failed_entries += 1
        continue

    quantity = int(entry)

    if quantity < 0:
        print("Negative numbers not allowed.")
        failed_entries += 1
        continue

    inventory += quantity

    print("Current inventory:", inventory)
    
    if inventory >500:
        print("Inventory limit exceeded!")
        break

print("Final inventory:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)
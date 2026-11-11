import io
from contextlib import redirect_stdout

from supplier import Supplier
from product import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory
from order import Order

LINE = "-" * 49

# PREDICTIONS for section 7, written before running the test:
# product_id -> (expected get_fulfilment_info(), expected specialised line)
PHYSICAL_INFO = "Physical product: requires storage and physical shipping."
DIGITAL_INFO = "Digital product: delivered electronically via download."
PREDICTIONS: dict[str, tuple[str, str]] = {
    "P1": (PHYSICAL_INFO, "Weight: 3.80 kg"),
    "P2": (PHYSICAL_INFO, "Weight: 2.00 kg"),
    "D1": (DIGITAL_INFO, "Download Size: 4500.00 MB"),
}


def heading(text: str) -> None:
    print(f"\n{LINE}\n{text}\n{LINE}")


def show_product_details(product: Product) -> None:
    """Works for ANY Product. It never checks which subclass it received."""
    product.display_information()
    print(product.get_fulfilment_info())


def check_stock_contract(product: Product) -> None:
    """The expectation Product sets for update_stock(): it sets stock to
    the new quantity, returns the change as an int, and rejects negatives
    with ValueError. Every subclass must meet it."""
    before = product.stock

    change = product.update_stock(before + 5)
    assert isinstance(change, int) and change == 5
    assert product.stock == before + 5

    change = product.update_stock(before)
    assert change == -5
    assert product.stock == before

    try:
        product.update_stock(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("Negative stock should raise ValueError")
    assert product.stock == before


supplier = Supplier("S1", "Test Supplier", "test@example.com")
guitar = PhysicalProduct("P1", "Guitar", 800.0, 2, supplier, 3.8)
software = DigitalProduct("D1", "Operating System", 129.0, 10, supplier, 4500.0)

# ---------------------------------------------------------------------------
# Section 6: LSP
# ---------------------------------------------------------------------------
heading("1. show_product_details() with both subclasses")
show_product_details(guitar)
print()
show_product_details(software)

heading("2. Both product types can be added to an Inventory")
inventory = Inventory()
assert inventory.add_product(guitar)
assert inventory.add_product(software)
assert not inventory.add_product(guitar)  # duplicate ID still rejected
print("Both added. Duplicate ID rejected for both kinds.")

heading("3. Inventory.display_all() asks each Product to display itself")
inventory.display_all()

heading("4. Normal Inventory operations work for both")
for pid in ("P1", "D1"):
    found = inventory.find_product(pid)
    assert found is not None
    assert inventory.update_stock(pid, found.stock + 3)
    print(f"{pid}: stock updated to {found.stock}")
for pid in ("P1", "D1"):
    found = inventory.find_product(pid)
    assert found is not None
    check_stock_contract(found)
print("update_stock() contract holds for both subclasses.")

heading("5. Both can be used in an Order")
order = Order("O1")
order.add_order_line(guitar, 1)
order.add_order_line(software, 2)
order.display_information()
assert order.calculate_total() == 800.0 + 2 * 129.0

heading("6. Both can be removed and re-added (aggregation)")
for pid in ("P1", "D1"):
    removed = inventory.remove_product(pid)
    assert removed is not None
    assert inventory.find_product(pid) is None
    assert inventory.add_product(removed)
print("Removed and re-added without destroying either product.")

print("\nAll LSP checks passed.")

# ---------------------------------------------------------------------------
# Section 7: Polymorphism
# ---------------------------------------------------------------------------
heading("7. Polymorphism: one loop over the Product collection")
poly_inventory = Inventory()
poly_inventory.add_product(
    PhysicalProduct("P1", "Guitar", 800.0, 2, supplier, 3.8))
poly_inventory.add_product(
    DigitalProduct("D1", "Operating System", 129.0, 10, supplier, 4500.0))
poly_inventory.add_product(
    PhysicalProduct("P2", "Keyboard", 99.0, 45, supplier, 2.0))

failures = 0
for product in poly_inventory.products:
    # Capture what display_information() prints so it can be checked.
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        product.display_information()
    displayed = buffer.getvalue()
    fulfilment = product.get_fulfilment_info()

    expected_fulfilment, expected_line = PREDICTIONS[product.product_id]
    fulfilment_ok = fulfilment == expected_fulfilment
    display_ok = expected_line in displayed
    failures += (not fulfilment_ok) + (not display_ok)

    print(displayed, end="")
    print(f"Fulfilment: {fulfilment}")
    print(f"  prediction matched (fulfilment): {fulfilment_ok}")
    print(f"  prediction matched (display):    {display_ok}")
    print(LINE)

assert failures == 0, f"{failures} prediction(s) did not match"
print("All predictions matched. Each object ran its own implementation.")
heading("8. Transfer a Product from one Inventory to another")
inventory_a = Inventory()
inventory_b = Inventory()
amp = PhysicalProduct("P9", "Amplifier", 300.0, 4, supplier, 9.5)
inventory_a.add_product(amp)
moved = inventory_a.remove_product("P9")
assert moved is amp
assert inventory_a.find_product("P9") is None
assert inventory_b.add_product(moved)
assert inventory_b.find_product("P9") is amp
assert amp.stock == 4 and amp.supplier is supplier
print("Product moved between inventories and still exists unchanged.")
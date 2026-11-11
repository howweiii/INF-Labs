from __future__ import annotations

from product import Product, product_from_dict
from supplier import Supplier

LINE: str = "-" * 49


class Inventory:
    """Manages a collection of Product objects (aggregation).

    The Inventory groups Products but does not create them or control
    their lifecycle. It only uses the Product interface, so it works the
    same for PhysicalProduct, DigitalProduct or any future subclass (LSP).
    """

    def __init__(self) -> None:
        # Typed with the base class so any kind of Product can be stored.
        self.__products: list[Product] = []
        self.__transactions: list[dict[str, object]] = []

    @property
    def products(self) -> list[Product]:
        """A copy of the product list, so callers can loop over every
        Product but cannot add or remove products behind the Inventory's
        back."""
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID already exists."""
        if self.find_product(product.product_id):
            return False
        self.__products.append(product)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "add",
             "amount": round(product.price * product.stock, 2)})
        return True

    def find_product(self, product_id: str) -> Product | None:
        """Return the matching Product, or None if it cannot be found."""
        for product in self.__products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the matching Product reference and return it (or None).
        The product itself is not destroyed, so it can be re-added or
        transferred."""
        product = self.find_product(product_id)
        if not product:
            return None
        self.__products.remove(product)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "remove",
             "amount": round(-product.price * product.stock, 2)})
        return product

    def find_supplier(self, supplier_id: str) -> Supplier | None:
        """Return an existing Supplier used by any product, or None.
        This only looks suppliers up; the Inventory does not own them."""
        for product in self.__products:
            if product.supplier.supplier_id.upper() == supplier_id.upper():
                return product.supplier
        return None

    def get_suppliers(self) -> list[Supplier]:
        """Return each distinct Supplier used by the products."""
        suppliers: dict[str, Supplier] = {}
        for product in self.__products:
            suppliers[product.supplier.supplier_id] = product.supplier
        return list(suppliers.values())

    def get_products_by_supplier(self, supplier_id: str) -> list[Product]:
        """Return the products supplied by the given supplier ID."""
        return [p for p in self.__products
                if p.supplier.supplier_id.upper() == supplier_id.upper()]

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Returns False if not found. Raises ValueError for bad quantity."""
        product = self.find_product(product_id)
        if not product:
            return False
        change = product.update_stock(new_stock)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "update",
             "amount": round(change * product.price, 2)})
        return True

    def assign_supplier(self, product_id: str, supplier: Supplier) -> bool:
        """Returns False if the product is not found. The Inventory only
        passes the Supplier to the Product; it does not own it."""
        product = self.find_product(product_id)
        if not product:
            return False
        product.set_supplier(supplier)
        return True

    def display_all(self) -> None:
        """Ask every Product to display itself. Each object chooses its own
        implementation, so no type checks are needed here."""
        print("\nCurrent Inventory")
        print(LINE)
        for product in self.products:
            product.display_information()
            print(LINE)

    def to_dict(self) -> dict[str, list]:
        # Each distinct supplier is saved once; products refer to it by ID.
        return {"suppliers": [s.to_dict() for s in self.get_suppliers()],
                "products": [p.to_dict() for p in self.__products],
                "transactions": self.__transactions}

    @classmethod
    def from_dict(cls, data: dict | list) -> Inventory:
        inventory = cls()
        if isinstance(data, list):
            data = {"products": data, "transactions": []}
        suppliers: dict[str, Supplier] = {}
        for item in data.get("suppliers", []):
            supplier = Supplier.from_dict(item)
            suppliers[supplier.supplier_id] = supplier
        for item in data.get("products", []):
            inventory.__products.append(product_from_dict(item, suppliers))
        inventory.__transactions = data.get("transactions", [])
        return inventory
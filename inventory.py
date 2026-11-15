from __future__ import annotations

from product import Product, product_from_dict
from supplier import Supplier

LINE: str = "-" * 49


class Inventory:

    def __init__(self) -> None:
        # Typed with the base class so any kind of Product can be stored.
        self.__products: list[Product] = []
        self.__transactions: list[dict[str, object]] = []

    @property
    def products(self) -> list[Product]:
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.product_id):
            return False
        self.__products.append(product)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "add",
             "amount": round(product.price * product.stock, 2)})
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if not product:
            return None
        self.__products.remove(product)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "remove",
             "amount": round(-product.price * product.stock, 2)})
        return product

    def find_supplier(self, supplier_id: str) -> Supplier | None:
        for product in self.__products:
            if product.supplier.supplier_id.upper() == supplier_id.upper():
                return product.supplier
        return None

    def get_suppliers(self) -> list[Supplier]:
        suppliers: dict[str, Supplier] = {}
        for product in self.__products:
            suppliers[product.supplier.supplier_id] = product.supplier
        return list(suppliers.values())

    def get_products_by_supplier(self, supplier_id: str) -> list[Product]:
        return [p for p in self.__products
                if p.supplier.supplier_id.upper() == supplier_id.upper()]

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        product = self.find_product(product_id)
        if not product:
            return False
        change = product.update_stock(new_stock)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "update",
             "amount": round(change * product.price, 2)})
        return True

    def assign_supplier(self, product_id: str, supplier: Supplier) -> bool:
        product = self.find_product(product_id)
        if not product:
            return False
        product.set_supplier(supplier)
        return True

    def display_all(self) -> None:
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
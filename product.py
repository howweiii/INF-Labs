from __future__ import annotations

from abc import ABC, abstractmethod

from supplier import Supplier

BASE_SHIPPING_COST: float = 5.00
COST_PER_KG: float = 2.00
UNKNOWN_SUPPLIER_ID: str = "S0"


# ---------------------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------------------
class Product(ABC):
    """Abstract base class for every product in the inventory."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if not str(product_id).strip():
            raise ValueError("Product ID cannot be empty.")
        if not str(name).strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        if not isinstance(supplier, Supplier):
            raise ValueError("A Product needs a Supplier object.")
        self.__product_id: str = str(product_id).strip()
        self.__name: str = str(name).strip()
        self.__price: float = price
        self.__stock: int = stock
        # Association: a reference to an independent Supplier object.
        self.supplier: Supplier = supplier

    # Read-only access from outside the class
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Describe how this product is delivered to the customer."""
        pass

    def update_stock(self, quantity: int) -> int:
        """Set stock to a new quantity. Returns the change in stock."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        change = quantity - self.__stock
        self.__stock = quantity
        return change

    def set_supplier(self, supplier: Supplier) -> None:
        """Associate this product with a different Supplier object."""
        if not isinstance(supplier, Supplier):
            raise ValueError("A Product needs a Supplier object.")
        self.supplier = supplier

    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.supplier.name}")

    def to_dict(self) -> dict[str, object]:
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock,
                "supplier_id": self.supplier.supplier_id}

    def __str__(self) -> str:
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock} | "
                f"Supplier: {self.supplier.name}")


# ---------------------------------------------------------------------------
# Interface-style contract
# ---------------------------------------------------------------------------
class CanBeShipped(ABC):
    """Interface-style contract: any class that can be shipped must be
    able to calculate its shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the shipping cost for this object."""
        pass


# ---------------------------------------------------------------------------
# Concrete product types
# ---------------------------------------------------------------------------
class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped. Adds a weight (kg)."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight: float = weight

    @property
    def weight(self) -> float:
        return self.__weight

    def get_fulfilment_info(self) -> str:
        return "Physical product: requires storage and physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Flat $5.00 plus $2.00 per kilogram."""
        return BASE_SHIPPING_COST + COST_PER_KG * self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict[str, object],
                  supplier: Supplier) -> PhysicalProduct:
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data.get("weight", 0.0))

    def __str__(self) -> str:
        return f"{super().__str__()} | Weight: {self.__weight:.2f} kg"


class DigitalProduct(Product):
    """A product delivered by download. Adds a download size (MB)."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier,
                 download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered electronically via download."

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict[str, object],
                  supplier: Supplier) -> DigitalProduct:
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data["download_size"])

    def __str__(self) -> str:
        return (f"{super().__str__()} | "
                f"Download Size: {self.__download_size:.2f} MB")


# ---------------------------------------------------------------------------
# Factory used when loading from JSON
# ---------------------------------------------------------------------------
# Maps the saved "type" identifier to the class that rebuilds it.
PRODUCT_TYPES: dict[str, type[PhysicalProduct] | type[DigitalProduct]] = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def product_from_dict(data: dict[str, object],
                      suppliers: dict[str, Supplier]) -> Product:
    """Create the right Product subclass from saved data.

    `suppliers` maps supplier_id -> Supplier (already built), so products
    that share a supplier share the same object.

    Data saved before Lab 7 has no "type", so it is treated as physical.
    Data saved before suppliers existed has no "supplier_id", so it is
    given a shared placeholder "Unknown Supplier".
    """
    product_type = data.get("type", "physical")
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type: {product_type}")

    supplier_id = data.get("supplier_id", UNKNOWN_SUPPLIER_ID)
    if supplier_id not in suppliers:
        if supplier_id != UNKNOWN_SUPPLIER_ID:
            raise ValueError(f"Unknown supplier: {supplier_id}")
        suppliers[UNKNOWN_SUPPLIER_ID] = Supplier(
            UNKNOWN_SUPPLIER_ID, "Unknown Supplier", "unknown@example.com")

    return PRODUCT_TYPES[product_type].from_dict(data, suppliers[supplier_id])
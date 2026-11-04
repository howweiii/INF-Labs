from product import Product
from shipping import Shipping

BASE_SHIPPING_COST = 5.00
COST_PER_KG = 2.00


class PhysicalProduct(Product, Shipping):
    """A product that is stored and shipped. Adds a weight (kg)."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    def get_fulfilment_info(self):
        return "Physical product: requires storage and physical shipping."

    def calculate_shipping_cost(self):
        """Flat $5.00 plus $2.00 per kilogram."""
        return BASE_SHIPPING_COST + COST_PER_KG * self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   data.get("weight", 0.0))

    def __str__(self):
        return f"{super().__str__()} | Weight: {self.__weight:.2f} kg"
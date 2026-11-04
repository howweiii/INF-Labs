from abc import ABC, abstractmethod


class Shipping(ABC):
    """Interface-style contract: any class that can be shipped must be
    able to calculate its shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this object."""
        pass
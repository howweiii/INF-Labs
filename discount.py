from __future__ import annotations

from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """A way of discounting an order total. Order only depends on this
    interface, so new discounts can be added without changing Order (OCP)."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Take an order total and return the discounted total."""
        pass

class NoDiscount(DiscountStrategy):
    """Returns the total unchanged."""

    def apply(self, total: float) -> float:
        return total

    def __str__(self) -> str:
        return "No discount"


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)

    def __str__(self) -> str:
        return f"{self.percentage:g}% off"


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold,
    e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")
        self.threshold: float = threshold
        self.amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            # Never let the discount push the total below zero.
            return max(total - self.amount, 0.0)
        return total

    def __str__(self) -> str:
        return f"${self.amount:.2f} off orders of ${self.threshold:.2f} or more"


class StudentDiscount(DiscountStrategy):
    """Section 2.4: a new strategy added WITHOUT changing Order.
    Students get 5% off, capped at a maximum saving (default $50)."""

    RATE: float = 0.05

    def __init__(self, max_saving: float = 50.0) -> None:
        if max_saving < 0:
            raise ValueError("Maximum saving cannot be negative.")
        self.max_saving: float = max_saving

    def apply(self, total: float) -> float:
        saving = min(total * self.RATE, self.max_saving)
        return total - saving

    def __str__(self) -> str:
        return f"Student 5% off (max ${self.max_saving:.2f})"
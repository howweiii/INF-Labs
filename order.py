from __future__ import annotations

from product import Product
from discount import DiscountStrategy, NoDiscount


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise ValueError("An order line needs a Product object.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return (f"{self.product.product_id} | {self.product.name} | "
                f"${self.product.price:.2f} x {self.quantity} = "
                f"${self.calculate_subtotal():.2f}")


class Order:

    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        if not str(order_id).strip():
            raise ValueError("Order ID cannot be empty.")
        self.order_id: str = str(order_id).strip()
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = NoDiscount()
        if discount is not None:
            self.set_discount(discount)

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:

        if not isinstance(discount, DiscountStrategy):
            raise ValueError("Discount must be a DiscountStrategy object.")
        self.__discount = discount

    @property
    def order_lines(self) -> list[OrderLine]:
       
        return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:

        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:

        for line in self.__order_lines:
            if line.product.product_id.upper() == product_id.upper():
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_subtotal(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

    def cancel(self) -> None:
        self.__order_lines.clear()

    def display_information(self) -> None:
        print(f"Order ID: {self.order_id}")
        if not self.__order_lines:
            print("  No order lines.")
        for line in self.__order_lines:
            print(f"  {line}")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Discount: {self.__discount}")
        print(f"Total: ${self.calculate_total():.2f}")
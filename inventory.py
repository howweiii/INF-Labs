from product import Product

LINE = "-" * 49


class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []
        self.__transactions = []

    def add_product(self, product):
        """Returns False if the ID already exists."""
        if self.search_product(product.product_id):
            return False
        self.__products.append(product)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "add",
             "amount": round(product.price * product.stock, 2)})
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def update_stock(self, product_id, new_stock):
        """Returns False if not found. Raises ValueError for bad quantity."""
        product = self.search_product(product_id)
        if not product:
            return False
        change = product.update_stock(new_stock)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "update",
             "amount": round(change * product.price, 2)})
        return True

    def remove_product(self, product_id):
        product = self.search_product(product_id)
        if not product:
            return False
        self.__products.remove(product)
        self.__transactions.append(
            {"product_id": product.product_id, "type": "remove",
             "amount": round(-product.price * product.stock, 2)})
        return True

    def display_all(self):
        print("\nCurrent Inventory")
        print(LINE)
        for product in self.__products:
            print(product)
        print(LINE)

    def to_dict(self):
        return {"products": [p.to_dict() for p in self.__products],
                "transactions": self.__transactions}

    @classmethod
    def from_dict(cls, data):
        inventory = cls()
        # Accept the old plain-list format as well as the new dict format
        if isinstance(data, list):
            data = {"products": data, "transactions": []}
        for item in data.get("products", []):
            inventory.__products.append(Product.from_dict(item))
        inventory.__transactions = data.get("transactions", [])
        return inventory
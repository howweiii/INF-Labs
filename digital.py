from product import Product

class DigitalProduct(Product):
    """A product delivered by download. Adds a download size (MB)."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    @property
    def download_size(self):
        return self.__download_size

    def get_fulfilment_info(self):
        return "Digital product: delivered electronically via download."

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   data["download_size"])

    def __str__(self):
        return (f"{super().__str__()} | "
                f"Download Size: {self.__download_size:.2f} MB")
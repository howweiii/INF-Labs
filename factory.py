from physical import PhysicalProduct
from digital import DigitalProduct

# Maps the saved "type" identifier to the class that rebuilds it.
PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def product_from_dict(data):
    """Create the right Product subclass from saved data.

    Data saved before Lab 7 has no "type", so it is treated as physical.
    """
    product_type = data.get("type", "physical")
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type: {product_type}")
    return PRODUCT_TYPES[product_type].from_dict(data)
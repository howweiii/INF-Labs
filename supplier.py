from __future__ import annotations


class Supplier:
    """Someone who supplies products. Exists independently of any Product."""

    def __init__(self, supplier_id: str, name: str,
                 contact_email: str) -> None:
        if not str(supplier_id).strip():
            raise ValueError("Supplier ID cannot be empty.")
        if not str(name).strip():
            raise ValueError("Supplier name cannot be empty.")
        if "@" not in str(contact_email):
            raise ValueError("Contact email must contain '@'.")
        self.supplier_id: str = str(supplier_id).strip()
        self.name: str = str(name).strip()
        self.contact_email: str = str(contact_email).strip()

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id}")
        print(f"Supplier Name: {self.name}")
        print(f"Contact Email: {self.contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {"id": self.supplier_id, "name": self.name,
                "contact_email": self.contact_email}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Supplier:
        # Files saved without an email still load, using a placeholder.
        return cls(data["id"], data["name"],
                   data.get("contact_email", "unknown@example.com"))

    def __str__(self) -> str:
        return f"{self.name} ({self.supplier_id})"
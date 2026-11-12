class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self._supplier_id: str = supplier_id
        self._name: str = name
        self._contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self._supplier_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def contact_email(self) -> str:
        return self._contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self._supplier_id} | Name: {self._name} | Email: {self._contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self._supplier_id,
            "name": self._name,
            "contact_email": self._contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Supplier":
        return cls(
            supplier_id=data["supplier_id"],
            name=data["name"],
            contact_email=data["contact_email"],
        )
from dataclasses import dataclass
from datetime import date
from typing import Any, Self


@dataclass
class Car:
    """id, registration_number, first_registration_date, vin, brand, model"""
    id: int = None
    registration_number: str = None
    first_registration_date: date = None
    vin: str = None
    brand: str = None
    model: str = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            int(data["id"]),
            data["registration_number"],
            date.fromisoformat(data["first_registration_date"]),
            data["vin"],
            data["brand"],
            data["model"]
        )

    @classmethod
    def attr_names(cls) -> list[str]:
        return ['id', 'registration_number', 'first_registration_date', 'vin', 'brand', 'model']

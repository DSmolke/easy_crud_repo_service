from dataclasses import dataclass
from datetime import date


@dataclass
class Order:
    id: int = None
    order_date: date = None

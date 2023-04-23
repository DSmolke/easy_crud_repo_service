from dataclasses import dataclass

@dataclass
class Team:
    id: int | None = None
    name: str | None = None
    points: int | None = 0

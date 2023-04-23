from dataclasses import dataclass

@dataclass
class Player:
    id: int | None = None
    name: str | None = None
    goals: int | None = 0
    team_id: int | None = None



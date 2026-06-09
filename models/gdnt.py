from dataclasses import dataclass, field

@dataclass
class GDnT:
    symbol: str
    tolerance: str | None = None
    datum_refs: list[str] = field(default_factory=list)
from dataclasses import dataclass

@dataclass
class Metadata:
    part_number: str | None = None
    revision: str | None = None
    material: str | None = None
    mass:  str | None = None
    author:  str | None = None
    status:  str | None = None
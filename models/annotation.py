from dataclasses import dataclass

@dataclass
class Annotation:
    text: str
    x: float | None = None
    y: float | None = None
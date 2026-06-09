from dataclasses import dataclass

@dataclass
class Issue:
    rule_id: str
    severity: str
    message: str

    object_type: str | None = None
    object_name: str | None = None

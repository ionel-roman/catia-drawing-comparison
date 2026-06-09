from dataclasses import dataclass, field
from models.view import View


@dataclass
class Sheet:

    name: str
    paper_size: str | None = None
    scale: float | None = None
    orientation: str | None = None

    views: list[View] = field(default_factory=list)

    def add_view(self, view: View):
        self.views.append(view)

    @property
    def view_count(self):
        return len(self.views)



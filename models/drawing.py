from dataclasses import dataclass, field
from models.sheet import Sheet
from models.parameter import Parameter
from models.metadata import Metadata

@dataclass
class Drawing:
    name: str
    file_path: str

    sheets: list[Sheet] = field(default_factory=list)
    parameters: dict[str, Parameter] = field(default_factory=dict)
    metadata: Metadata = field(default_factory=Metadata)

    def add_sheet(self, sheet: Sheet):
        self.sheets.append(sheet)

    @property
    def sheet_count(self):
        return len(self.sheets)
    
    def get_all_views(self):
        views = []

        for sheet in self.sheets:
            views.extend(sheet.views)

            return views

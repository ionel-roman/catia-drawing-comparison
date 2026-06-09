from dataclasses import dataclass, field
from models.dimension import Dimension
from models.annotation import Annotation
from models.gdnt import GDnT


@dataclass
class View:
    name: str
    view_type: str | None = None
    scale: float | None = None
    
    dimensions: list[Dimension] = field(default_factory=list)
    annotations: list[Annotation] = field(default_factory=list)
    gdnts: list[GDnT] = field(default_factory=list)

    x: float | None = None
    z: float | None = None

    def add_dimension(self, dimension: Dimension):
        self.dimensions.append(dimension)
    def add_annotation(self, annotation: Annotation):
        self.annotations.append(annotation)
    def add_gdnt(self, gdnt: GDnT):
        self.gdnts.append(gdnt)
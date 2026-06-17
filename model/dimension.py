from dataclasses import dataclass
from typing import Optional

@dataclass
class Dimension:
    sheet: str
    view:str
    name: str
    value:float
    dim_type: str
    upper_tol:Optional[float] = None
    lower_tol:Optional[float] = None
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class CellHeader:
    type: str
    arguments: Dict[str, Any]


@dataclass
class Cell:
    header: CellHeader
    content: str

from abc import ABC, abstractmethod, abstractstaticmethod
from typing import List
from pandoc.types import Pandoc


class AbstractCell(ABC):
    """Defines the abstract cell type that Leko uses."""
    @abstractstaticmethod
    def get_tags() -> List[str]:
        return []

    @abstractmethod
    def render_cell(self) -> Pandoc:
        pass

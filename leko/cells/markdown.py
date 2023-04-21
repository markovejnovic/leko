from typing import List

import pandoc
from pandoc.types import Pandoc, Meta, CodeBlock
from leko.cells.base import AbstractCell
from leko.cells.rendering import merge_renders
from leko.cells.type import Cell


class MarkdownCell(AbstractCell):
    """Defines a Markdown cell."""
    @staticmethod
    def get_tags() -> List[str]:
        return ["md", "markdown"]

    def render_cell(self, cell: Cell) -> Pandoc:
        markdown_render: Pandoc = pandoc.read(cell.content)

        if cell.header.arguments.get('output-only'):
            return markdown_render

        source_render = Pandoc(Meta({}), [
            CodeBlock(('', ['markdown'], []), cell.content)
        ])

        # If we have to render the source as well, then:
        return merge_renders((source_render, markdown_render))

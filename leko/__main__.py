from os import path
import sys
from leko.cells.exec import ExecCell
from leko.cells.markdown import MarkdownCell
import pandoc

from leko.cells import parser as cell_parser

CELL_HANDLERS = [
    MarkdownCell,
    ExecCell,
]


def _main():
    """Entry point."""
    with open(path.realpath(sys.argv[1]), 'r') as f:
        file_content = f.read()

    for cell in cell_parser.parse(file_content):
        handler = next(
            h for h in CELL_HANDLERS if cell.header.type in  h.get_tags())()
        pandoc.write(handler.render_cell(cell), file='test.pdf', format='pdf')


if __name__ == '__main__':
    _main()

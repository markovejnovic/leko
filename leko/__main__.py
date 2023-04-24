from os import path
import sys
from leko.cells.exec import ExecCell
from leko.cells.markdown import MarkdownCell
import pandoc

from leko.cells import parser as cell_parser
from leko.cells.rendering import merge_renders
import argparse

CELL_HANDLERS = [
    MarkdownCell,
    ExecCell,
]


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description='A notebook command-line application',
    )
    parser.add_argument(
        'input_file',
        metavar='IN',
        help='The input .leko file source. If \'-\' is specified, reads from' +
             'stdin until EOF.')
    parser.add_argument('-o', '--output', help='The output file.',
                        required=True)
    parser.add_argument('-f', '--format', help='The output file format.')
    args = parser.parse_args()

    # Read input file
    if args.input_file == '-':
        file_content = sys.stdin.read()
    else:
        with open(path.realpath(args.input_file), 'r') as f:
            file_content = f.read()

    cell_renders = [
        next(h for h in CELL_HANDLERS
             if cell.header.type in h.get_tags()
        )().render_cell(cell)
        for cell in cell_parser.parse(file_content)
    ]

    pandoc.write(merge_renders(cell_renders), file=args.output,
                 format=args.format)


if __name__ == '__main__':
    main()

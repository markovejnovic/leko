from os import path
import sys
from typing import Dict, Tuple
from leko.cells.exec import ExecCell
from leko.cells.markdown import MarkdownCell
import pandoc
from pandoc.types import Pandoc

from leko.cells import parser as cell_parser
from leko.cells.rendering import merge_renders
import argparse
import pkg_resources
import multiprocessing as mp
import time

from leko.cells.type import Cell

CELL_HANDLERS = [
    MarkdownCell,
    ExecCell,
]

STYLES: Dict[str, str] = {
    'pdf': pkg_resources.resource_filename('leko', 'style/default.tex'),
    'latex': pkg_resources.resource_filename('leko', 'style/default.tex')
}

def mp_render(id_c: Tuple[int, Cell]) -> Pandoc:
    id, c = id_c
    beg = time.time()
    render = next(h for h in CELL_HANDLERS
                if c.header.type in h.get_tags())().render_cell(c)
    t = time.time() - beg
    print(f'Processing cell: {id} took {t} seconds', file=sys.stderr)
    return render

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
    parser.add_argument(
        '-f', '--format',
        help='The output file format. Currently supported: \'pdf\'',
        required=True
    )
    args = parser.parse_args()

    # Read input file
    if args.input_file == '-':
        file_content = sys.stdin.read()
    else:
        with open(path.realpath(args.input_file), 'r') as f:
            file_content = f.read()

    render_pool = mp.Pool(mp.cpu_count())
    cell_renders = render_pool.map(
        mp_render,
        enumerate(cell_parser.parse(file_content)))

    pandoc.write(merge_renders(cell_renders), file=args.output,
                 format=args.format, options=[
                     '-V', 'linkcolor:blue',
                     '-V', 'geometry:a4paper',
                     '-V', 'geometry:margin=1in',
                     '-H', STYLES[args.format]
                     ]
    )


if __name__ == '__main__':
    main()

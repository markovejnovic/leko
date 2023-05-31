from os import path
import sys
from typing import Dict, Tuple
from leko.cells.exec import ExecCell
from leko.cells.markdown import MarkdownCell
import pandoc
from pandoc.types import Pandoc

from leko.cells import parser as cell_parser
from leko.cells.rendering import merge_renders
from leko import cli, timing
import pkg_resources
import multiprocessing as mp
import itertools
from leko.cells.type import Cell

CELL_HANDLERS = [
    MarkdownCell,
    ExecCell,
]

STYLES: Dict[str, str] = {
    'pdf': pkg_resources.resource_filename('leko', 'style/default.tex'),
    'latex': pkg_resources.resource_filename('leko', 'style/default.tex')
}

def mp_render(id_c: Tuple[int, Cell], verbose: bool = False) -> Pandoc:
    id, c = id_c
    with timing.Timer(verbose,
                      f'Processing cell: {id} took {{time:.3f}} seconds.'):
        render = next(h for h in CELL_HANDLERS
                      if c.header.type in h.get_tags())().render_cell(c)
    return render

def main():
    """Entry point."""
    args = cli.args()

    # Read input file
    if args.input_file == '-':
        file_content = sys.stdin.read()
    else:
        with open(path.realpath(args.input_file), 'r') as f:
            file_content = f.read()

    with mp.Pool(args.jobs) as render_pool:
        cell_renders = render_pool.starmap(
            mp_render,
            zip(enumerate(cell_parser.parse(file_content)),
                itertools.repeat(args.verbose))
        )

    with timing.Timer(args.verbose, 'Linking cells took {time:.3f} seconds.'):
        pandoc.write(merge_renders(cell_renders), file=args.output,
                     format=args.format, options=[
                         '-V', 'linkcolor:blue',
                         '-V', 'geometry:a4paper',
                         '-V', 'geometry:margin=1in',
                         '-H', STYLES[args.format]
                         ])


if __name__ == '__main__':
    main()

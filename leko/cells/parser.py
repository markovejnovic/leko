from dataclasses import dataclass
from typing import Any, Generator, Iterable, List, Tuple

from leko.cells.type import Cell, CellHeader

CELL_TOKEN = '---'


@dataclass
class _CellSplit:
    content: str
    header: str
    index: int


def _split_cells(content: str) -> List[_CellSplit]:
    outs: List[_CellSplit] = []
    current_cell = _CellSplit('', '', -1)
    for line in content.splitlines():
        if line.startswith(CELL_TOKEN):
            # We have found a new cell, push the previous one.
            if current_cell.index != -1:
                outs.append(current_cell)

            # A new cell is found.
            current_cell = _CellSplit('', line[len(CELL_TOKEN):],
                                      current_cell.index + 1)

            continue
        # Append the content
        current_cell.content += (line + '\n')

    # Always append the last cell.
    if current_cell.index != -1:
        outs.append(current_cell)

    print(outs)
    return outs


def parse_header(header_str: str) -> CellHeader:
    arg_separator = ','
    kv_separator = '='

    def parse_args(
        args_split: Iterable[str]
    ) -> Generator[Tuple[str, Any], None, None]:
        for a in args_split:
            if kv_separator in a:
                yield tuple(a.split(kv_separator, 1))
            yield (a, True)

    spl = header_str.strip().split(arg_separator)
    return CellHeader(spl[0], { k: v for k, v in parse_args(spl[1:]) })


def _parse_cell(cell: _CellSplit) -> Cell:
    return Cell(parse_header(cell.header), cell.content)


def _parse_cells(cells: Iterable[_CellSplit]) -> Generator[Cell, None, None]:
    return (_parse_cell(c) for c in cells)


def parse(raw: str) -> Generator[Cell, None, None]:
    return _parse_cells(_split_cells(raw))

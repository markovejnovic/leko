from typing import Iterable
from pandoc.types import Pandoc, Meta


def merge_renders(renders: Iterable[Pandoc]) -> Pandoc:
    """Merges multiple renders (ie. multiple cell render outputs) to a single
    render.
    """
    out_pandoc = Pandoc(Meta({}), [])
    for render in renders:
        # TODO(markovejnovic): Kind of a nasty hack
        out_pandoc._args[1] = out_pandoc._args[1] + render._args[1]
    return out_pandoc

from typing import List
from leko.cells.base import AbstractCell
from leko.cells.rendering import merge_renders
from leko.cells.type import Cell
import tempfile
import subprocess
from pandoc.types import Pandoc, Meta, CodeBlock, RawBlock
import os
import stat


class ExecCell(AbstractCell):
    """Defines an executor cell."""
    @staticmethod
    def get_tags() -> List[str]:
        return ["exec"]

    def render_cell(self, cell: Cell) -> Pandoc:
        # Unpack arguments
        coding = (
            'utf8'
            if (cd := cell.header.arguments.get('coding')) is None
            else (cd if isinstance(cd, str) else 'utf8')
        )
        syntax = '' if (s := cell.header.arguments.get('stx')) is None else s
        
        raw_str = cell.content
        with tempfile.NamedTemporaryFile('w+', delete=False) as script:
            # Dump the exec script to a temp file
            script.write(raw_str)
        # Update the +x bit
        os.chmod(script.name, os.stat(script.name).st_mode | stat.S_IEXEC)

        output_render = Pandoc(Meta({}), [
            CodeBlock(('', [], []), 'Could not render the output.')
        ])

        popen = subprocess.Popen((script.name, ), stdout=subprocess.PIPE)
        popen.wait()
        if popen.stdout is not None:
            execution_out = popen.stdout.read()
            exec_output = execution_out.decode(coding)
            output_render = Pandoc(Meta({}), [
                CodeBlock(('', [], []), exec_output)
            ])

        if cell.header.arguments.get('output-only'):
            return 

        source_render = Pandoc(Meta({}), [
            CodeBlock(('', [syntax], []), cell.content)
        ])

        return merge_renders((source_render, output_render))

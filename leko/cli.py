"""This module defines the CLI interface to leko."""

import argparse
import multiprocessing

PROGRAM_DESCRIPTION = "Cell-based notebook"

def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)

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

    parser.add_argument(
        '-v', '--verbose',
        help='Output debugging info.',
        required=False,
        action='store_true'
    )

    parser.add_argument(
        '-j', '--jobs',
        help=('Specify the number of jobs to run simultaneously. Defaults to '
              'the number of available CPU cores.'),
        required=False,
        type=int,
        default=multiprocessing.cpu_count()
    )

    return parser.parse_args()

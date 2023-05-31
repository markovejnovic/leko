"""Exposes easy-to-use timing utility functions."""

import time


DEFAULT_TIMER_PRINTOUT = "Time taken: {time:.3f} seconds."

class Timer:
    """Performs timing of the enclosed routine."""

    def __init__(self, verbose: bool = False,
                 printout_template: str = DEFAULT_TIMER_PRINTOUT) -> None:
        self.verbose = verbose
        self.start_time = None
        self.end_time = None
        self.printout_template = printout_template

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, *_):
        self.end_time = time.time()

        if self.verbose:
            self.__print_time()

    def time(self) -> float:
        """Returns the amount of time taken in the with block."""
        if self.start_time is None or self.end_time is None:
            raise RuntimeError("The Timer has not been executed in a with "
                               "block.")
        return self.end_time - self.start_time

    def __print_time(self) -> None:
        print(self.printout_template.format(time=self.time()))

from typing import Generator


def getMatrixValGen(path: str) -> Generator[float, None, None]:
    # returns float generator
    # float used as int is subset of type
    with open(path) as f:
        for line in f:
            for value in line.split():
                yield float(value)

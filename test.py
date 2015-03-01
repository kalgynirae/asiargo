"""Do some basic mathy things."""

from asiargo import allez_cuisine, command

@command
def add(a: int, b: int = 1, *, verbose=False):
    """Sum two integers"""
    if verbose:
        print("The sum is: ", end="")
    print(a + b)

@command
def subtract(*numbers: int):
    """Subtract some integers"""
    first, *rest = numbers
    print(first - sum(rest))

if __name__ == '__main__':
    allez_cuisine(__doc__)

import sys

from asiargo import allez_cuisine, command

@command
def add(a: int, b: int = 5, *, dry_run: bool = False):
    """Sum two integers"""
    if dry_run:
        print("It's a dry run!")
    print(a + b)

if __name__ == '__main__':
    sys.exit(allez_cuisine(__doc__))

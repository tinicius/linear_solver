import sys
from src.solver.solve import solve
from src.solver.read_file import read_file


def main():
    if len(sys.argv) < 2:
        raise ValueError("Please provide a filename as an argument.")

    filename = sys.argv[1]

    solve(*read_file(filename))


if __name__ == "__main__":
    main()

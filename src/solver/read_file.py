import numpy as np


def read_file(filename: str):
    with open(filename, 'r') as file:
        [n, m] = file.readline().split()

        c = np.array(file.readline().split(), dtype=float)

        A = []
        b = []

        for line in file:
            numbers = list(map(float, line.strip().split()))
            A.append(numbers[:-1])
            b.append(numbers[-1])

    return int(n), int(m), c, np.array(A), np.array(b)

from typing import TypedDict, List
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


class LPInput(TypedDict):
    e: int  # Number of constraints
    n: int  # Number of variables
    op: int  # Operation type (1 for minimization, 2 for maximization)
    objective: List[int]  # Objective function coefficients
    a: List[List[int]]  # Coefficients of the constraints
    b: List[int]  # Right-hand side values of the constraints


def read_input(file_path: str) -> LPInput:
    with open(file_path, "r") as f:
        lines = f.readlines()

    n, e, op = map(int, lines[0].split())

    objective = list(map(int, lines[1].strip().split()))

    a = []
    b = []

    for i in range(2, len(lines)):
        line = lines[i].strip().split()
        a.append(list(map(int, line[:-1])))
        b.append(int(line[-1]))

    return LPInput(e=e, n=n, op=op, objective=objective, a=a, b=b)


def get_pairs(n: int) -> List[tuple]:
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((i, j))
    return pairs


def get_filled_area(points: List[tuple]) -> tuple:
    # Compute centroid
    centroid = points.mean(axis=0)

    # Compute angle of each point relative to centroid
    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])

    # Sort points by angle
    sorted_points = points[np.argsort(angles)]

    # Unpack x and y
    x, y = sorted_points[:, 0], sorted_points[:, 1]

    return x, y


def get_value(objective: List[int], params: List[int]) -> int:
    value = 0
    for i in range(len(objective)):
        value += objective[i] * params[i]
    return value


def solve(problem: LPInput):

    extra = 0

    for i in range(len(problem["a"])):
        extra += 1

        for u in range(len(problem["a"])):
            if u == i:
                problem["a"][i].append(1)
            else:
                problem["a"][i].append(0)

    a = np.array(problem["a"])
    b = np.array(problem["b"])

    pairs = get_pairs(problem["n"] + extra)

    valid_pairs = []
    invalid_pairs = []

    solution = []
    best = 0

    for i, j in pairs:
        _a = a.copy()

        _a[:, i] = 0
        _a[:, j] = 0

        x, residuals, rank, s = np.linalg.lstsq(_a, b, rcond=None)

        if not np.any(x < 0):
            valid_pairs.append((x[0], x[1]))

            value = get_value(problem["objective"], x)

            if (value > best) or (best == 0):
                best = value
                solution = x

        else:
            invalid_pairs.append((x[0], x[1]))

    for i, j in valid_pairs:
        if (i == solution[0] and j == solution[1]) or (
            i == solution[1] and j == solution[0]
        ):
            plt.plot(i, j, "o", color="green", zorder=2)
            continue

        plt.plot(i, j, "o", color="blue", zorder=2)

    for i, j in invalid_pairs:
        plt.plot(i, j, "o", color="red", zorder=2)

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="Valid Pair",
            markerfacecolor="blue",
            markersize=10,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="Solution",
            markerfacecolor="green",
            markersize=10,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="Invalid Pair",
            markerfacecolor="red",
            markersize=10,
        ),
    ]

    x, y = get_filled_area(np.array(valid_pairs))
    plt.fill(x, y, color="skyblue", alpha=0.6)

    for i, constraint in enumerate(a):

        coeffs = [-constraint[0] / constraint[1], b[i] / constraint[1]]

        poly = np.poly1d(coeffs)

        x = np.linspace(0, 200, 400)

        y = poly(x)

        plt.plot(x, y, label=f"y = {poly}", color="black", zorder=1)

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Polynomial Function")
    plt.grid(True)
    plt.legend(handles=legend_elements)
    plt.axhline(0, color="black", zorder=1)  # x-axis
    plt.axvline(0, color="black", zorder=1)  # y-axis
    plt.show()


problem = read_input("input")

solve(problem)

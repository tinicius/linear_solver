import numpy as np
from itertools import combinations


def solve(n: int, m: int, c: np.ndarray, A: np.ndarray, b: np.ndarray):
    """
        `n`: Número de variáveis \n
        `m`: Número de restrições \n
        `c`: Coeficientes da função objetivo \n
        `A`: Coeficientes das restrições \n
        `b`: Limites das restrições \n
    """

    if m >= n:
        raise ValueError(
            "Number of constraints must be less than number of variables")

    total = 0
    valid_count = 0
    invalid_count = 0

    best = np.inf
    best_x = None

    for comb in combinations(range(n), n - m):

        _A = np.delete(A, comb, axis=1)

        try:
            x = np.linalg.solve(_A, b)
        except np.linalg.LinAlgError:
            continue

        total += 1

        valid = (x >= 0).all()

        valid_text = ""

        if valid:
            valid_count += 1
            valid_text = "viável"
        else:
            invalid_count += 1
            valid_text = "inviável"

        _c = np.delete(c, comb)

        z = np.dot(_c, x)

        for bi in comb:
            x = np.insert(x, bi, 0)

        if valid and z < best:
            best = z
            best_x = x

        print(f"x = {x}")
        print(f"z = {z} ({valid_text})")

        print()

    print(f"Número total de soluções básicas: {total}")
    print(f"Número de soluções básicas viáveis: {valid_count}")
    print(f"Número de soluções básicas inviáveis: {invalid_count}")
    print()

    if best_x is not None:
        print("Solução ótima encontrada!")
        print(f"Função objetivo = {best}")
        print(f"x = {best_x}")
    else:
        print("Nenhuma solução ótima encontrada!")

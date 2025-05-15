import numpy as np
from itertools import combinations


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


def solve(n: int, m: int, c: np.ndarray, A: np.ndarray, b: np.ndarray):
    
    if m >= n:
        raise ValueError("Number of constraints must be less than number of variables")

    total = 0
    valid_count = 0
    invalid_count = 0
    
    best = np.inf
    best_x = None
    
    for comb in combinations(range(n), n - m):
        _A = np.copy(A)
        
        for i in comb:
            _A[:, i] = 0
            
        rank_A = np.linalg.matrix_rank(_A)
        rank_aug = np.linalg.matrix_rank(np.hstack((_A, b.reshape(-1, 1))))

        if rank_A < rank_aug:
            continue
            
        total += 1    
            
        x, residuals, rank, s = np.linalg.lstsq(_A, b, rcond=None)

        x = np.round(x, 2)

        valid = (x >= 0).all()
        
        valid_text = ""
        
        if valid:
            valid_count += 1
            valid_text = "viável"
        else:
            invalid_count += 1
            valid_text = "inviável"
        
        z = np.dot(c, x)
        
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


solve(*read_file("input.txt"))

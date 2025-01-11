import numpy as np
import solve_sudoku as ss

data = np.array([
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],

    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0]
    ])

data = np.array([
    [8,0,3, 0,0,0, 0,2,0],
    [0,0,0, 0,9,0, 0,0,0],
    [0,0,0, 0,0,1, 0,6,0],
    
    [0,0,2, 7,0,0, 0,0,0],
    [0,0,5, 6,0,0, 0,0,0],
    [0,3,0, 0,0,0, 9,0,8],

    [0,9,0, 0,3,0, 2,0,0],
    [3,1,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,5,0]
    ])

try:
    design = data.copy()
    s = ss.design_ppt(design)
    print(f"Unsolved design = {s}")
    design2 = ss.solve_sudoku(design)
    s2 = ss.design_ppt(design2)
    print(f"Solved design = {s2}")
except:
    print(f"No solution")


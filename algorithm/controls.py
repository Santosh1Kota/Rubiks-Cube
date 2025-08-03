# Global list to track all moves made
moves_made = []

def print_moves():
    """Print all moves made so far"""
    print("Moves made:", " ".join(moves_made))

def rotate_face_clockwise(face_grid):
    """Rotate a 3x3 face 90 degrees clockwise."""
    return [[face_grid[2-j][i] for j in range(3)] for i in range(3)]

def rotate_face_counterclockwise(face_grid):
    """Rotate a 3x3 face 90 degrees counterclockwise."""
    return [[face_grid[j][2-i] for j in range(3)] for i in range(3)]

def F(cube):
    """F move: Front face clockwise (z = 1, dir = -1 in Processing)"""
    moves_made.append("F")
    # Rotate the F face itself clockwise
    cube.faces['F'] = rotate_face_counterclockwise(cube.faces['F'])
    temp1 = []
    for inner_list in cube.faces['L']:
        temp1.append(inner_list[-1])
    #print(temp1)
    for i in range(3):
        cube.faces['L'][i][2] = cube.faces['U'][2][2-i]
    temp2 = cube.faces['D'][0].copy()
    temp2 =temp2[::-1]
    print(temp2)
    for i in range(3):
        cube.faces['D'][0][i] = temp1[i]
    temp1 = []
    for inner_list in cube.faces['R']:
        temp1.append(inner_list[0])
    for i in range(3):
        cube.faces['R'][i][0] = temp2[i]
    for i in range(3):
        cube.faces['U'][2][i] = temp1[i]


def F_prime(cube):
    """F' move: Front face counterclockwise (z = 1, dir = 1 in Processing)"""
    moves_made.append("F'")
    # Rotate the F face itself clockwise (opposite of F)
    cube.faces['F'] = rotate_face_clockwise(cube.faces['F'])
    
    # Reverse cycle: U -> R -> D -> L -> U
    temp1 = []
    for inner_list in cube.faces['R']:
        temp1.append(inner_list[0])  # Save R left column
    reversed(temp1)
    for i in range(3):
        cube.faces['R'][i][0] = cube.faces['U'][2][i]  # R left column <- U bottom row (reversed)
    
    temp2 = cube.faces['D'][0].copy()  # Save D top row
    temp1 = temp1[::-1]
    for i in range(3):
        cube.faces['D'][0]= temp1  # D top row <- R left column (saved)
    
    temp1 = []
    for inner_list in cube.faces['L']:
        temp1.append(inner_list[-1])  # Save L right column
    reversed(temp1)
    for i in range(3):
        cube.faces['L'][i][2] = temp2[i]  # L right column <- D top row (saved, reversed)
    
    for i in range(3):
        cube.faces['U'][2][i] = temp1[2-i]  # U bottom row <- L right column (saved)

def B(cube):
    """B move: Back face clockwise (z = -1, dir = 1 in Processing)"""
    moves_made.append("B")
    # Rotate the B face itself clockwise
    cube.faces['B'] = rotate_face_counterclockwise(cube.faces['B'])
    
    temp1 = []
    for inner_list in cube.faces['R']:
        temp1.append(inner_list[-1])  # Save R left column
    reversed(temp1)
    for i in range(3):
        cube.faces['R'][i][2] = cube.faces['U'][0][i]  # R left column <- U bottom row (reversed)
    
    temp2 = cube.faces['D'][2].copy()  # Save D top row
    temp1 = temp1[::-1]
    for i in range(3):
        cube.faces['D'][2]= temp1  # D top row <- R left column (saved)
    
    temp1 = []
    for inner_list in cube.faces['L']:
        temp1.append(inner_list[0])  # Save L right column
    reversed(temp1)
    for i in range(3):
        cube.faces['L'][i][0] = temp2[i]  # L right column <- D top row (saved, reversed)
    
    for i in range(3):
        cube.faces['U'][0][i] = temp1[2-i]  # U bottom row <- L right column (saved)


def B_prime(cube):
    """B' move: Back face counterclockwise (z = -1, dir = -1 in Processing)"""
    moves_made.append("B'")
    # Rotate the B face itself counterclockwise
    cube.faces['B'] = rotate_face_clockwise(cube.faces['B'])
    temp1 = []
    for inner_list in cube.faces['L']:
        temp1.append(inner_list[0])
    #print(temp1)
    for i in range(3):
        cube.faces['L'][i][0] = cube.faces['U'][0][2-i]
    temp2 = cube.faces['D'][-1].copy()
    temp2 =temp2[::-1]
    #print(temp2)
    for i in range(3):
        cube.faces['D'][-1][i] = temp1[i]
    temp1 = []
    for inner_list in cube.faces['R']:
        temp1.append(inner_list[-1])
    for i in range(3):
        cube.faces['R'][i][-1] = temp2[i]
    for i in range(3):
        cube.faces['U'][0][i] = temp1[i]

def U(cube):
    """U move: Up face clockwise (x = -1, dir = 1 in Processing)"""
    moves_made.append("U")
    # Rotate the U face itself clockwise
    cube.faces['L'] = rotate_face_counterclockwise(cube.faces['L'])
    temp1 = []
    for inner_list in cube.faces['B']:
        temp1.append(inner_list[-1])
    #print(temp1)
    for i in range(3):
        cube.faces['B'][i][2] = cube.faces['U'][2-i][0]
    temp2 = []
    for inner_list in cube.faces['D']:
        temp2.append(inner_list[0])
    for i in range(3):
        cube.faces['D'][i][0] = temp1[2-i]
    temp1 = []
    for inner_list in cube.faces['F']:
        temp1.append(inner_list[0])
    for i in range(3):
        cube.faces['F'][i][0] = temp2[i]
    for i in range(3):
        cube.faces['U'][i][0] = temp1[i]

def U_prime(cube):
    """U' move: Up face counterclockwise (x = -1, dir = -1 in Processing)"""
    moves_made.append("U'")
    # Rotate the U face itself counterclockwise
    cube.faces['L'] = rotate_face_clockwise(cube.faces['L'])
    temp1 = []
    for inner_list in cube.faces['B']:
        temp1.append(inner_list[-1])
    #print(temp1)
    for i in range(3):
        cube.faces['B'][i][2] = cube.faces['D'][2-i][0]
    temp2 = []
    for inner_list in cube.faces['U']:
        temp2.append(inner_list[0])
    for i in range(3):
        cube.faces['U'][i][0] = temp1[2-i]
    temp1 = []
    for inner_list in cube.faces['F']:
        temp1.append(inner_list[0])
    for i in range(3):
        cube.faces['F'][i][0] = temp2[i]
    for i in range(3):
        cube.faces['D'][i][0] = temp1[i]

def D(cube):
    """D move: Down face clockwise (x = 1, dir = -1 in Processing)"""
    moves_made.append("D")
    # Rotate the D face itself clockwise
    cube.faces['R'] = rotate_face_counterclockwise(cube.faces['R'])
    temp1 = []
    for inner_list in cube.faces['B']:
        temp1.append(inner_list[0])
    #print(temp1)
    for i in range(3):
        cube.faces['B'][i][0] = cube.faces['D'][2-i][2]
    temp2 = []
    for inner_list in cube.faces['U']:
        temp2.append(inner_list[2])
    for i in range(3):
        cube.faces['U'][i][2] = temp1[2-i]
    temp1 = []
    for inner_list in cube.faces['F']:
        temp1.append(inner_list[2])
    for i in range(3):
        cube.faces['F'][i][2] = temp2[i]
    for i in range(3):
        cube.faces['D'][i][2] = temp1[i]
    

def D_prime(cube):
    """D' move: Down face counterclockwise (x = 1, dir = 1 in Processing)"""
    moves_made.append("D'")
    # Rotate the D face itself counterclockwise
    cube.faces['R'] = rotate_face_clockwise(cube.faces['R'])
    temp1 = []
    for inner_list in cube.faces['B']:
        temp1.append(inner_list[0])
    #print(temp1)
    for i in range(3):
        cube.faces['B'][i][0] = cube.faces['U'][2-i][2]
    temp2 = []
    for inner_list in cube.faces['D']:
        temp2.append(inner_list[2])
    for i in range(3):
        cube.faces['D'][i][2] = temp1[2-i]
    temp1 = []
    for inner_list in cube.faces['F']:
        temp1.append(inner_list[2])
    for i in range(3):
        cube.faces['F'][i][2] = temp2[i]
    for i in range(3):
        cube.faces['U'][i][2] = temp1[i]
    

def L(cube):
    """L move: Left face clockwise (y = 1, dir = 1 in Processing)"""
    moves_made.append("L")
    # Rotate the L face itself clockwise
    cube.faces['D'] = rotate_face_counterclockwise(cube.faces['D'])
    temp1 = cube.faces['B'][2].copy()
    cube.faces['B'][2] = cube.faces['L'][2]
    temp2 = cube.faces['R'][2].copy()
    cube.faces['R'][2] = temp1
    temp1 = cube.faces['F'][2].copy()
    cube.faces['F'][2] = temp2
    cube.faces['L'][2] = temp1

    

def L_prime(cube):
    """L' move: Left face counterclockwise (y = 1, dir = -1 in Processing)"""
    moves_made.append("L'")
    # Rotate the L face itself counterclockwise
    cube.faces['D'] = rotate_face_clockwise(cube.faces['D'])
    temp1 = cube.faces['B'][2].copy()
    cube.faces['B'][2] = cube.faces['R'][2]
    temp2 = cube.faces['L'][2].copy()
    cube.faces['L'][2] = temp1
    temp1 = cube.faces['F'][2].copy()
    cube.faces['F'][2] = temp2
    cube.faces['R'][2] = temp1

    

def R(cube):
    """R move: Right face clockwise (y = -1, dir = -1 in Processing)"""
    moves_made.append("R")
    # Rotate the R face itself clockwise
    cube.faces['U'] = rotate_face_counterclockwise(cube.faces['U'])
    temp1 = cube.faces['B'][0].copy()
    cube.faces['B'][0] = cube.faces['R'][0]
    temp2 = cube.faces['L'][0].copy()
    cube.faces['L'][0] = temp1
    temp1 = cube.faces['F'][0].copy()
    cube.faces['F'][0] = temp2
    cube.faces['R'][0] = temp1
    print("RAN R")

def R_prime(cube):
    """R' move: Right face counterclockwise (y = -1, dir = 1 in Processing)"""
    moves_made.append("R'")
    # Rotate the R face itself counterclockwise
    cube.faces['U'] = rotate_face_clockwise(cube.faces['U'])
    temp1 = cube.faces['B'][0].copy()
    cube.faces['B'][0] = cube.faces['L'][0]
    temp2 = cube.faces['R'][0].copy()
    cube.faces['R'][0] = temp1
    temp1 = cube.faces['F'][0].copy()
    cube.faces['F'][0] = temp2
    cube.faces['L'][0] = temp1
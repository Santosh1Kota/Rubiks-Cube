# Global list to track all moves made
moves_made = []
# Separate list for unfiltered/raw moves (for debugging)
moves = []
def anim_move_convert():
    move_map = {
        "U": "L'",
        "U'": "L",
        "D": "R'",
        "D'": "R",
        "L": "F'",
        "L'": "F",
        "R": "B'",
        "R'": "B",
        "F": "U'",
        "F'": "U",
        "B": "D'",
        "B'": "D",
    }

    def translate_move(m: str) -> str:
        return move_map.get(m, m)
    moves_animcube = [translate_move(m) for m in moves_made]
    print("Anim moves made:", " ".join(moves_made))
    return moves_animcube
def add_move(move):
    """Add a move to the moves_made list with optimizations"""
    moves.append(move)  # Keep raw unfiltered moves for debugging
    
    # Check if last move would be opposite of the current last move
    if len(moves_made) >= 1:
        # Map moves to their opposites
        opposite_moves = {
            "F": "F'", "F'": "F",
            "B": "B'", "B'": "B", 
            "U": "U'", "U'": "U",
            "D": "D'", "D'": "D",
            "L": "L'", "L'": "L", 
            "R": "R'", "R'": "R"
        }
        
        # If the new move is opposite of the last move, remove the last move instead of adding
            
        if moves[-1] == "B" or moves[-1] == "B'":
            if opposite_moves.get(add_move) == move:
                print("oppoos")
                print(moves_made[-1],move)
                print(moves_made)

                moves_made.pop()  # Remove last move
                return  # Exit early, no need for other optimizations
    
    # Check if adding this move would make 4 identical moves (360° = no change)
    if len(moves_made) >= 3 and moves_made[-1] == moves_made[-2] == moves_made[-3] == move:
        print("3 identical")
        print(moves_made[-1],moves_made[-2],moves_made[-3],move)
        # Remove the last 3 identical moves instead of adding the 4th
        moves_made.pop()
        moves_made.pop()
        moves_made.pop()
        return  # Exit early, no need to check for 3-move optimization
    
    # Check if adding this move would make 3 identical moves (can be optimized to opposite)
    if len(moves_made) >= 2 and moves_made[-1] == moves_made[-2] == move:
        print_moves()
        print("2 identical")
        print(moves_made[-1],moves_made[-2],move)
        # Remove the last 2 identical moves
        moves_made.pop()
        moves_made.pop()
        
        # Map moves to their opposites
        opposite_moves = {
            "F": "F'", "F'": "F",
            "B": "B'", "B'": "B", 
            "U": "U'", "U'": "U",
            "D": "D'", "D'": "D",
            "L": "L'", "L'": "L", 
            "R": "R'", "R'": "R"
        }
        
        # Add the opposite move instead
        opposite = opposite_moves.get(move)
        print("opposite",opposite)
        moves_made.append(opposite)
        return
    
    # If no optimizations applied, add the move normally
    moves_made.append(move)


def print_moves():
    """Print all moves made so far"""
    print("Moves made:", " ".join(moves_made))

def export_moves() -> dict:
    """Export current move history for APIs (raw and optimized)."""
    # Mapping from your fixed-world moves to AnimCube3.js moves
    move_map = {
        "U": "L'",
        "U'": "L",
        "D": "R'",
        "D'": "R",
        "L": "F'",
        "L'": "F",
        "R": "B'",
        "R'": "B",
        "F": "U'",
        "F'": "U",
        "B": "D'",
        "B'": "D",
    }

    def translate_move(m: str) -> str:
        return move_map.get(m, m)
    moves_animcube = [translate_move(m) for m in moves_made]
    print("Anim moves made:", " ".join(moves_made))
    return {
        "moves": list(moves),
        "moves_made": list(moves_made),
        "moves_animcube": moves_animcube,
        "count": len(moves_made),
    }

def clear_moves():
    """Clear both move logs."""
    moves_made.clear()
    moves.clear()

def rotate_face_clockwise(face_grid):
    """Rotate a 3x3 face 90 degrees clockwise."""
    return [[face_grid[2-j][i] for j in range(3)] for i in range(3)]

def rotate_face_counterclockwise(face_grid):
    """Rotate a 3x3 face 90 degrees counterclockwise."""
    return [[face_grid[j][2-i] for j in range(3)] for i in range(3)]

def F(cube, do_not_append: bool = False):
    """F move: Front face clockwise (z = 1, dir = -1 in Processing)"""
    if not do_not_append:
        add_move("F")
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


def F_prime(cube, do_not_append: bool = False):
    """F' move: Front face counterclockwise (z = 1, dir = 1 in Processing)"""
    if not do_not_append:
        add_move("F'")
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

def B(cube, do_not_append: bool = False):
    """B move: Back face clockwise (z = -1, dir = 1 in Processing)"""
    if not do_not_append:
        add_move("B")
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


def B_prime(cube, do_not_append: bool = False):
    """B' move: Back face counterclockwise (z = -1, dir = -1 in Processing)"""
    if not do_not_append:
        add_move("B'")
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

def U(cube, do_not_append: bool = False):
    """U move: Up face clockwise (x = -1, dir = 1 in Processing)"""
    if not do_not_append:
        add_move("U")
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

def U_prime(cube, do_not_append: bool = False):
    """U' move: Up face counterclockwise (x = -1, dir = -1 in Processing)"""
    if not do_not_append:
        add_move("U'")
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

def D(cube, do_not_append: bool = False):
    """D move: Down face clockwise (x = 1, dir = -1 in Processing)"""
    if not do_not_append:
        add_move("D")
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
    

def D_prime(cube, do_not_append: bool = False):
    """D' move: Down face counterclockwise (x = 1, dir = 1 in Processing)"""
    if not do_not_append:
        add_move("D'")
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
    

def L(cube, do_not_append: bool = False):
    """L move: Left face clockwise (y = 1, dir = 1 in Processing)"""
    if not do_not_append:
        add_move("L")
    # Rotate the L face itself clockwise
    cube.faces['D'] = rotate_face_counterclockwise(cube.faces['D'])
    temp1 = cube.faces['B'][2].copy()
    cube.faces['B'][2] = cube.faces['L'][2]
    temp2 = cube.faces['R'][2].copy()
    cube.faces['R'][2] = temp1
    temp1 = cube.faces['F'][2].copy()
    cube.faces['F'][2] = temp2
    cube.faces['L'][2] = temp1

    

def L_prime(cube, do_not_append: bool = False):
    """L' move: Left face counterclockwise (y = 1, dir = -1 in Processing)"""
    if not do_not_append:
        add_move("L'")
    # Rotate the L face itself counterclockwise
    cube.faces['D'] = rotate_face_clockwise(cube.faces['D'])
    temp1 = cube.faces['B'][2].copy()
    cube.faces['B'][2] = cube.faces['R'][2]
    temp2 = cube.faces['L'][2].copy()
    cube.faces['L'][2] = temp1
    temp1 = cube.faces['F'][2].copy()
    cube.faces['F'][2] = temp2
    cube.faces['R'][2] = temp1

    

def R(cube, do_not_append: bool = False):
    """R move: Right face clockwise (y = -1, dir = -1 in Processing)"""
    if not do_not_append:
        add_move("R")
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

def R_prime(cube, do_not_append: bool = False):
    """R' move: Right face counterclockwise (y = -1, dir = 1 in Processing)"""
    if not do_not_append:
        add_move("R'")
    # Rotate the R face itself counterclockwise
    cube.faces['U'] = rotate_face_clockwise(cube.faces['U'])
    temp1 = cube.faces['B'][0].copy()
    cube.faces['B'][0] = cube.faces['L'][0]
    temp2 = cube.faces['R'][0].copy()
    cube.faces['R'][0] = temp1
    temp1 = cube.faces['F'][0].copy()
    cube.faces['F'][0] = temp2
    cube.faces['L'][0] = temp1
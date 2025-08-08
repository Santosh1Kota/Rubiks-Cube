import algorithm
import controls

def run_control(cube, control, direction):
    if control == "U" :
        if direction == "counterclockwise" or direction =="":
            controls.U(cube)
        else:
            controls.U_prime(cube)
    elif control == "D":
        if direction == "counterclockwise" or direction =="":
            controls.D(cube)
        else:
            controls.D_prime(cube)
    elif control == "L":
        if direction == "counterclockwise" or direction =="":
            controls.L(cube)
        else:
            controls.L_prime(cube)
    elif control == "R":
        if direction == "counterclockwise" or direction =="":
            controls.R(cube)
        else:
            controls.R_prime(cube)
    elif control == "B":
        if direction == "counterclockwise" or direction =="":
            controls.B(cube)
        else:
            controls.B_prime(cube)
    elif control == "F":
        if direction == "counterclockwise" or direction =="":
            controls.F(cube)
        else:
            controls.F_prime(cube)
    else:
        raise ValueError("Invalid control in run_control")

def solve_middle_edge(cube, color1, color2):
    """Solve a single middle layer edge"""
    color2face = {"RED": "R", "YELLOW": "B", "ORANGE": "L", "GREEN": "D", "BLUE": "U", "WHITE": "F"}
    on_right = {"L":"D","D":"R","R":"U","U":"L"}
    
    if cube.is_middle_edge_in_correct_position(color1, color2):
        print("edge already in correct position")
        return;
    
    info = cube.find_edge_with_colors(color1, color2)
    
    if info['face1'] == 'B' or info['face2'] == 'B':
        print("B")
        one_to_use, other = sort_one_to_use(info)
        print(one_to_use)
        print(other)
        cube.visualize()
        while(one_to_use['face'] != color2face.get(one_to_use['color'])):
            controls.B(cube)
            info = cube.find_edge_with_colors(color1, color2)
            one_to_use, other = sort_one_to_use(info)
        print("dracula")
        if on_right.get(one_to_use['face']) == color2face.get(other['color']):
            print("right")
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(other['color']),True)
            controls.B(cube)
            run_control(cube, face_to_move, direction)
            controls.B_prime(cube)
            run_control(cube, face_to_move, "clockwise")
            controls.B_prime(cube)
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(one_to_use['color']),True)
            run_control(cube, face_to_move, "clockwise")
            controls.B(cube)
            run_control(cube, face_to_move, "counterclockwise")
        else:
            print("left")
            cube.visualize()
            print(one_to_use)
            print(other)
            controls.print_moves()
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(other['color']),True)
            controls.B_prime(cube)
            run_control(cube, face_to_move, "clockwise")
            controls.B(cube)
            run_control(cube, face_to_move, "counterclockwise")
            controls.B(cube)
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(one_to_use['color']),True)
            run_control(cube, face_to_move, "counterclockwise")
            controls.B_prime(cube)
            run_control(cube, face_to_move, "clockwise")
            controls.print_moves()
    else:
        #code in morning, if the one you want to use is entered wrong, assign a temp variable to the one at the bottom on the same side and run either transformation to get it out and then run the right transofrmation
        #all you need to figure out is how to find what is currently in the position that is on one of the color's faces, and the other on the bottom face. 
        one_to_use, other = sort_one_to_use(info)
        print(one_to_use)
        to_get_temp = {"L":((1,0),(1,2)),"D":((2,1),(2,1)),"R":((1,2),(1,0)),"U":((0,1),(0,1))}
        
        # Unpack the tuples to get row,col coordinates
        pos1, pos2 = to_get_temp[one_to_use['face']]
        temp_color1 = cube.faces[one_to_use['face']][pos1[0]][pos1[1]]
        temp_color2 = cube.faces['B'][pos2[0]][pos2[1]]
        print(color1, color2)
        print(temp_color1, temp_color2)
        print(on_right.get(one_to_use['face']) == color2face.get(other['color']))
        print("done")
        if not ((on_right.get(one_to_use['face']) == color2face.get(other['color']))):
            print("ah")
            controls.print_moves()
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(other['color']),True)
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(other['color']),True)
            controls.B(cube)
            run_control(cube, face_to_move, direction)
            controls.B_prime(cube)
            run_control(cube, face_to_move, "clockwise")
            controls.B_prime(cube)
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(one_to_use['color']),True)
            run_control(cube, face_to_move, "clockwise")
            controls.B(cube)
            run_control(cube, face_to_move, "counterclockwise")
            controls.print_moves()
        else:
            print("djsjd")
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(other['color']),True)
            controls.B_prime(cube)
            run_control(cube, face_to_move, "clockwise")
            controls.B(cube)
            run_control(cube, face_to_move, "counterclockwise")
            controls.B(cube)
            face_to_move,direction = cube.get_face_to_move_from_color_2(color2face.get(one_to_use['color']),True)
            run_control(cube, face_to_move, "counterclockwise")
            controls.B_prime(cube)
            run_control(cube, face_to_move, "clockwise")
            controls.print_moves()
        controls.print_moves()
        print(color1, color2)
        solve_all_middle_edges(cube)
def sort_one_to_use(info):
    one_to_use = {}
    other = {}
    keys1 = ['face1', 'position1', 'color1']
    keys2 = ['face2', 'position2', 'color2']
    if info['face1'] == 'B':
        for key in keys2:
            one_to_use[key[:-1]] = info[key]
        for key in keys1:
            other[key[:-1]] = info[key]
    else:
        for key in keys1:
            one_to_use[key[:-1]] = info[key]
        for key in keys2:
            other[key[:-1]] = info[key]
    return one_to_use, other

def solve_all_middle_edges(cube):
    # """Solve all 4 middle layer edges"""
    
    list_of_edges = [
        ["RED", "BLUE"],
        ["BLUE", "ORANGE"],
        ["ORANGE", "GREEN"],
        ["GREEN", "RED"]
    ]
    
    # Filter out edges that are already solved
    unsolved_edges = []
    for edge in list_of_edges:
        if not cube.is_middle_edge_in_correct_position(edge[0], edge[1]):
            unsolved_edges.append(edge)
    
    print(f"Edges already solved: {len(list_of_edges) - len(unsolved_edges)}")
    print(f"Edges needing solving: {unsolved_edges}")
    print("Unsolved edges",unsolved_edges)
    
    # Now work with unsolved_edges instead of list_of_edges
    priority_edges = []  # Edges on bottom face (priority)
    normal_edges = []    # Edges not on bottom face
    
    # Separate edges based on whether they're on bottom face
    for edge in unsolved_edges:
        info = cube.find_edge_with_colors(edge[0], edge[1])
        if info['face1'] == 'B' or info['face2'] == 'B':
            priority_edges.append(edge)  # Bottom face = priority
        else:
            normal_edges.append(edge)    # Not on bottom = normal
    
    # Combine: priority first, then normal
    order = priority_edges + normal_edges
    
    print("Priority (bottom face):", priority_edges)
    print("Normal (other positions):", normal_edges)
    print("Final order:", order)
    
    for edge in order:
        print(f"Processing: {edge}")
        solve_middle_edge(cube, edge[0], edge[1])
        
        
    cube.visualize()
    controls.print_moves()
    

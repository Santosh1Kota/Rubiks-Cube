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

def solve_yellow(cube):
    all_positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
    yellow_count = 0
    for pos in all_positions:
        if cube.faces['B'][pos[0]][pos[1]] == "YELLOW":
            yellow_count += 1
    
    if yellow_count == 9:
        print("🎉 Yellow face completely solved!")
        return
    
    # Edge positions on face B
    edge_positions = [(0,1), (1,0), (1,2), (2,1)]  # top, left, right, bottom
    
    # Corner positions on face B
    corner_positions = [(0,0), (0,2), (2,0), (2,2)]  # top-left, top-right, bottom-left, bottom-right
    
    # Count yellow edges
    yellow_edges = []
    for pos in edge_positions:
        if cube.faces['B'][pos[0]][pos[1]] == "YELLOW":
            yellow_edges.append(pos)
    
    # Count yellow corners
    yellow_corners = []
    for pos in corner_positions:
        if cube.faces['B'][pos[0]][pos[1]] == "YELLOW":
            yellow_corners.append(pos)
    
    print(f"Yellow edges found: {len(yellow_edges)} at positions {yellow_edges}")
    print(f"Yellow corners found: {len(yellow_corners)} at positions {yellow_corners}")
    
    # Helper to refresh local yellow positions
    def get_yellow_positions(c):
        edge_positions = [(0,1), (1,0), (1,2), (2,1)]
        corner_positions = [(0,0), (0,2), (2,0), (2,2)]
        edges = [p for p in edge_positions if c.faces['B'][p[0]][p[1]] == "YELLOW"]
        corners = [p for p in corner_positions if c.faces['B'][p[0]][p[1]] == "YELLOW"]
        return edges, corners
    if len(yellow_edges)==0:
        side_algorithm(cube)
        yellow_edges, yellow_corners = get_yellow_positions(cube)
        solve_yellow(cube)
    if len(yellow_edges)==4 and len(yellow_corners)==0:
        count =0
        while not cube.faces['R'][2][2] == "YELLOW":
            controls.B_prime(cube)
            count+=1
            if count == 4:
                success = main_algorithm(cube,"D")
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                if success:
                    return
                break
        if cube.faces['R'][2][2] == "YELLOW":
            success = main_algorithm(cube,"D")
            yellow_edges, yellow_corners = get_yellow_positions(cube)
            if success:
                return

    '''
    '''


    if len(yellow_corners) == 2 and len(yellow_edges) == 4:
        print("troy3")
        cube.visualize()
        print("FOUND 2 YELLOW CORNERS AND 4 YELLOW EDGES")
        corner1 = yellow_corners[0]
        corner2 = yellow_corners[1]
        
        # Check if corners are diagonal (neither row nor column match)
        if corner1[0] == corner2[0] or corner1[1] == corner2[1]:
            diagonal = False  # Same row or same column
        else:
            diagonal = True   # Diagonal corners
        if diagonal:
            #rotate B until it looks like this:
            target_pattern = [
                ['YELLOW', 'YELLOW', '-'],
                ['YELLOW', 'YELLOW', 'YELLOW'], 
                ['-', 'YELLOW', 'YELLOW']
            ]
            face_to_use = "D"
            # Check if face B already matches the pattern
            while not matches_pattern(cube, 'B', target_pattern):
                controls.B_prime(cube)
            success = main_algorithm(cube, face_to_use)
            yellow_edges, yellow_corners = get_yellow_positions(cube)
            if success:
                return
        else:
            face_to_use = "D"
            
            target_pattern = [
                ['-', 'YELLOW', 'YELLOW'],
                ['YELLOW', 'YELLOW', 'YELLOW'], 
                ['-', 'YELLOW', 'YELLOW']
            ]
            while not matches_pattern(cube, 'B', target_pattern):
                controls.B_prime(cube)
            cube.visualize()
            print("beforeza",face_to_use)
            success = main_algorithm(cube, face_to_use)
            cube.visualize()
            print("afterza",face_to_use)
            yellow_edges, yellow_corners = get_yellow_positions(cube)
            solve_yellow(cube)

        
        
        

    # Check for 2 adjacent yellow edges (like in side_algorithm)
    if len(yellow_edges) == 2:
        # Check if the 2 edges are adjacent (using same logic as side_algorithm)
        possible_adjacent_pairs = [((0,1),(1,0)), ((0,1),(1,2)), ((1,0),(2,1)), ((1,2),(2,1))]
        adjacent_pairs_dict = {
            ((0,1),(1,0)): "D",
            ((0,1),(1,2)): "R",
            ((1,0),(2,1)): "L",
            ((1,2),(2,1)): "U",
        }
        adjacent = False
        
        for pair in possible_adjacent_pairs:
            if set(pair) == set(yellow_edges):
                adjacent = True
                success = side_algorithm(cube, adjacent_pairs_dict.get(pair))
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                if success:
                    return
                solve_yellow(cube)
                
        
        # If we get here, the 2 edges are not adjacent
        if not adjacent:
            if cube.faces['B'][0][1] =="YELLOW" and cube.faces['B'][2][1] =="YELLOW":
                side_algorithm(cube, "R")
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                solve_yellow(cube)
            elif cube.faces['B'][1][0] =="YELLOW" and cube.faces['B'][1][2] =="YELLOW":
                side_algorithm(cube, "U")
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                solve_yellow(cube)
        
    
    # Check for all 4 yellow edges with no yellow corners
    elif len(yellow_edges) == 4 and len(yellow_corners) == 0:
        success = main_algorithm(cube, "R")  # Pass random face "R"
        yellow_edges, yellow_corners = get_yellow_positions(cube)
        if success:
            return
        
    
    # Check for all 4 yellow edges with exactly 1 yellow corner
    elif len(yellow_edges) == 4 and len(yellow_corners) == 1:
        position_locator = {(0,2):(0,1), (0,0):(1,0), (2,0):(2,1), (2,2):(1,2)}
        if cube.faces['B'][0][0] == "YELLOW":
            info_corner = cube.get_corner_from_position("B", (0,0))
            info_edge = cube.get_edge_from_position("B", position_locator.get((0,0)))
        elif cube.faces['B'][0][2] == "YELLOW":
            info_corner = cube.get_corner_from_position("B", (0,2))
            info_edge = cube.get_edge_from_position("B", position_locator.get((0,2)))
        elif cube.faces['B'][2][0] == "YELLOW":
            info_corner = cube.get_corner_from_position("B", (2,0))
            info_edge = cube.get_edge_from_position("B", position_locator.get((2,0)))
        elif cube.faces['B'][2][2] == "YELLOW":
            info_corner = cube.get_corner_from_position("B", (2,2))
            info_edge = cube.get_edge_from_position("B", position_locator.get((2,2)))
        else:
            raise ValueError("No yellow corner found")
        opposite_face = {"R":"L","L":"R","U":"D","D":"U"}
        if info_corner['face1'] == info_edge['face2']:
            face_to_use = info_corner['face1']
            one_to_use = {"R":(2,2),"U":(0,2),"D":(2,0),"L":(0,0)}
            position_to_use = one_to_use.get(face_to_use)
            if cube.faces[face_to_use][position_to_use[0]][position_to_use[1]] == "YELLOW":
                success = main_algorithm(cube, face_to_use)
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                if success:
                    return
            else:
                success = main_algorithm(cube, face_to_use)
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                if success:
                    return
                success = main_algorithm(cube, opposite_face.get(face_to_use))
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                if success:
                    return
            edge_count, corner_count = count_yellow_pieces(cube)
            if edge_count!=3 and corner_count !=3:
                success = main_algorithm(cube, face_to_use)
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
            
        elif info_corner['face2'] == info_edge['face2']:
            face_to_use = info_corner['face2']
            one_to_use = {"R":(2,2),"U":(0,2),"D":(2,0),"L":(0,0)}
            position_to_use = one_to_use.get(face_to_use)
            if cube.faces[face_to_use][position_to_use[0]][position_to_use[1]] == "YELLOW":
                success = main_algorithm(cube, face_to_use)
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                if success:
                    return
            else:
                success = main_algorithm(cube, face_to_use)
                if success:
                    return
                success = main_algorithm(cube, opposite_face.get(face_to_use))
                yellow_edges, yellow_corners = get_yellow_positions(cube)
                if success:
                    return
            edge_count, corner_count = count_yellow_pieces(cube)
        else:
            raise ValueError("No matching pattern found")

    else:
        print(f"No matching pattern found - {len(yellow_edges)} edges, {len(yellow_corners)} corners")
        main_algorithm(cube, "R")
        yellow_edges, yellow_corners = get_yellow_positions(cube)
    
    # Check if yellow face is completely solved (all 9 positions should be yellow)
    all_positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
    yellow_count = 0
    for pos in all_positions:
        if cube.faces['B'][pos[0]][pos[1]] == "YELLOW":
            yellow_count += 1
    
    if yellow_count == 9:
        print("🎉 Yellow face completely solved!")
        return
    else:
        print(f"Yellow face not complete ({yellow_count}/9 yellow) - running solve_yellow again...")
        edge_count, corner_count = count_yellow_pieces(cube)
        print(f"After side_algorithm: {edge_count} edges, {corner_count} corners")
        #solve_yellow(cube)
    if count_yellow_pieces(cube)[0]+count_yellow_pieces(cube)[1] == 8:
        edge_count, corner_count = count_yellow_pieces(cube)
        total_count = edge_count + corner_count
        print(f"🔍 DEBUG: Found {edge_count} edges + {corner_count} corners = {total_count} total")
        print("🔍 DEBUG: Condition met (== 8), returning...")
        cube.visualize()
        return
    
    # If we get here, total is not 8
    
    edge_count, corner_count = count_yellow_pieces(cube)
    total_count = edge_count + corner_count
    print(f"🔍 DEBUG: Current count is {edge_count} edges + {corner_count} corners = {total_count} total (not 8)")
    print("COUNT: ",count_yellow_pieces(cube)[0]+count_yellow_pieces(cube)[1])
    solve_yellow(cube)  # Recursive call


def side_algorithm(cube, face_to_use = None):
    if len(controls.moves) > 500:
        print("TOO MANY MOVES")
        exit()

    #Do algorithm that is not really the main one but the one we use to use before the main one. 
    #We only call this when there is  at least three yellow edges on one side. In the format.
    print("RUNNING SIDE ALGORITHM")
    color2face = {"RED": "R", "YELLOW": "B", "ORANGE": "L", "GREEN": "D", "BLUE": "U", "WHITE": "F"}
    reverse_on_right = {"D":"L","R":"D","U":"R","L":"U"}
    possible_outcomes = [[(0,1),(1,0)],[(0,1),(1,2)],[(1,0),(2,1)],[(1,2),(2,1)]]
    for outcome in possible_outcomes:
        # Get the actual colors at those positions on face B
        color1 = cube.faces['B'][outcome[0][0]][outcome[0][1]]
        color2 = cube.faces['B'][outcome[1][0]][outcome[1][1]]
        
        # Check if both colors belong to face B (i.e., both are YELLOW)
        if "B" == color2face.get(color1) and "B" == color2face.get(color2):
            # Both positions have YELLOW colors, continue with algorithm
            info1 = cube.get_edge_from_position("B", outcome[0])    
            info2 = cube.get_edge_from_position("B", outcome[1])
            if face_to_use is None:
                face_to_use = align_face(cube, info1, info2)
            #R' B' D' B D R
            control, direction = cube.get_face_to_move_from_color_2(face_to_use, False)
            print(control, direction)
            run_control(cube, control, direction)
            controls.B_prime(cube)
            control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(face_to_use), False)
            run_control(cube, control, direction)
            controls.B(cube)
            control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(face_to_use), True)
            run_control(cube, control, direction)
            control, direction = cube.get_face_to_move_from_color_2(face_to_use, True)
            run_control(cube, control, direction)
            cube.visualize()
            controls.print_moves()
            break
    else:
        import random
        faces = ["U", "R", "L", "D"]
        face_to_use = random.choice(faces)
        control, direction = cube.get_face_to_move_from_color_2(face_to_use, False)
        print(control, direction)
        print("before random")
        cube.visualize()
        
        run_control(cube, control, direction)
        controls.B_prime(cube)
        control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(face_to_use), False)
        run_control(cube, control, direction)
        controls.B(cube)
        control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(face_to_use), True)
        run_control(cube, control, direction)
        control, direction = cube.get_face_to_move_from_color_2(face_to_use, True)
        run_control(cube, control, direction)
        print("after random")
        cube.visualize()
        controls.print_moves()
    
    # Check if desired condition is met
    edge_count, corner_count = count_yellow_pieces(cube)
    total_count = edge_count + corner_count
    
    if total_count == 8:  # or whatever your condition is
        print(f"🎉 Side algorithm success! Reached target: {edge_count} edges + {corner_count} corners = {total_count}")
        return True  # Success flag
    else:
        print(f"Side algorithm not yet complete: {edge_count} edges + {corner_count} corners = {total_count}")
        return False  # Continue flag


def main_algorithm(cube, face):
    if len(controls.moves) > 500:
        print("TOO MANY MOVES")
        exit()
    """Main algorithm for yellow face solving"""
    # TODO: Implement main algorithm
    print(f"Running main_algorithm with face: {face}")
    #Imagine U came in
    color2face = {"RED": "R", "YELLOW": "B", "ORANGE": "L", "GREEN": "D", "BLUE": "U", "WHITE": "F"}
    reverse_on_right = {"D":"L","R":"D","U":"R","L":"U"}
    control1, direction1 = cube.get_face_to_move_from_color_2(reverse_on_right.get(face), False)
    print(control1, direction1)
    control2, direction2 = cube.get_face_to_move_from_color_2(reverse_on_right.get(face), True)
    #print("DISCH",control, direction)
    print("MAIN ALGORITHM:before")
    controls.print_moves()
    run_control(cube, control1, direction1)
    controls.B_prime(cube)
    run_control(cube, control2, direction2)
    controls.B_prime(cube)
    run_control(cube, control1, direction1)
    controls.B_prime(cube)
    controls.B_prime(cube)
    run_control(cube, control2, direction2)
    controls.print_moves()
    print("MAIN ALGORITHM:after")
    controls.print_moves()
    
    # Check if desired condition is met
    edge_count, corner_count = count_yellow_pieces(cube)
    total_count = edge_count + corner_count
    
    if total_count == 8:  # or whatever your condition is
        print(f"🎉 Success! Reached target: {edge_count} edges + {corner_count} corners = {total_count}")
        return True  # Success flag
    else:
        print(f"Not yet complete: {edge_count} edges + {corner_count} corners = {total_count}")
        return False  # Continue flag





def align_face(cube, info1, info2):
    print(info1)
    print(info2)
    reverse_on_right = {"D":"L","R":"D","U":"R","L":"U"}
    if reverse_on_right.get(info1['face2']) == info2['face2']:
        align_face = reverse_on_right.get(info2['face2'])
        return align_face
    else:
        if reverse_on_right.get(info2['face2']) == info1['face2']:
            align_face = reverse_on_right.get(info1['face2']) 
            return align_face
        else:
            raise ValueError("Invalid outcome")       
        
def matches_pattern(cube, face, pattern):
    """
    Check if a face matches a pattern where '-' means "don't care"
    Pattern should be a 3x3 list of lists like:
    [['Y', 'Y', '-'],
     ['Y', 'Y', 'Y'], 
     ['-', 'Y', 'Y']]
    """
    for row in range(3):
        for col in range(3):
            expected = pattern[row][col]
            actual = cube.faces[face][row][col]
            
            # Skip positions marked with '-' (don't care)
            if expected == '-':
                continue
                
            # Check if the expected color matches actual color
            if expected != actual:
                return False
    
    return True 

def recognizes_rotated_pattern(cube):
    """
    Efficiently recognize the specific pattern on face B regardless of rotation.
    Pattern: 4 yellow edges, 2 yellow corners (diagonal), specific arrangement.
    """
    face = cube.faces['B']
    
    # First, quick check: must have exactly 4 yellow edges and 2 yellow corners
    edge_count, corner_count = count_yellow_pieces(cube)
    if edge_count != 4 or corner_count != 2:
        return False, -1
    
    # Get yellow corner positions
    yellow_corners = []
    corner_positions = [(0,0), (0,2), (2,0), (2,2)]
    for pos in corner_positions:
        if face[pos[0]][pos[1]] == "YELLOW":
            yellow_corners.append(pos)
    
    # Must be diagonal corners
    corner1, corner2 = yellow_corners[0], yellow_corners[1]
    if corner1[0] == corner2[0] or corner1[1] == corner2[1]:
        return False, -1  # Not diagonal
    
    # Check which diagonal it is and determine rotation
    if set(yellow_corners) == {(0,0), (2,2)}:
        # Main diagonal: check if (0,1), (1,0), (1,2), (2,1) are yellow and (0,2), (2,0) are not
        if (face[0][1] == "YELLOW" and face[1][0] == "YELLOW" and 
            face[1][2] == "YELLOW" and face[2][1] == "YELLOW" and
            face[0][2] != "YELLOW" and face[2][0] != "YELLOW"):
            return True, 0  # Standard orientation
            
    elif set(yellow_corners) == {(0,2), (2,0)}:
        # Anti-diagonal: check if edges are yellow and other corners are not
        if (face[0][1] == "YELLOW" and face[1][0] == "YELLOW" and 
            face[1][2] == "YELLOW" and face[2][1] == "YELLOW" and
            face[0][0] != "YELLOW" and face[2][2] != "YELLOW"):
            return True, 2  # 180° rotation
    
    return False, -1
        

def count_yellow_pieces(cube):
    """Count yellow edges and corners on face B and return the counts"""
    # Edge positions on face B
    edge_positions = [(0,1), (1,0), (1,2), (2,1)]  # top, left, right, bottom
    
    # Corner positions on face B  
    corner_positions = [(0,0), (0,2), (2,0), (2,2)]  # top-left, top-right, bottom-left, bottom-right
    
    # Count yellow edges
    yellow_edges = 0
    for pos in edge_positions:
        if cube.faces['B'][pos[0]][pos[1]] == "YELLOW":
            yellow_edges += 1
    
    # Count yellow corners
    yellow_corners = 0
    for pos in corner_positions:
        if cube.faces['B'][pos[0]][pos[1]] == "YELLOW":
            yellow_corners += 1
    
    return yellow_edges, yellow_corners

def solve_all_yellow_face(cube):
    """Solve the entire yellow face (both cross and corners)"""
    # First solve the yellow cross
    print(len(controls.moves))
    print("ALL HAIL")
    for i in range(1):
        cube.visualize()
        print("After run #",i)
        solve_yellow(cube)
        cube.visualize()


    #test_pattern_recognition()



    
    # Then orient the yellow corners
    #solve_yellow_corners(cube)
    
    #print("Yellow face solving complete!")
    #controls.print_moves() 


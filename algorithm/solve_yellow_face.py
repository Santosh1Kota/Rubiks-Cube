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
    if len(yellow_edges)==4 and len(yellow_corners)==0:
        count =0
        while not cube.faces['R'][2][2] == "YELLOW":
            controls.B_prime(cube)
            count+=1
            if count == 4:
                success = main_algorithm(cube,"D")
                edge_count, corner_count = count_yellow_pieces(cube)
                print(f"After main_algorithm: {edge_count} edges, {corner_count} corners")
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
                print("could not find yellow edge on R")
                break
        if cube.faces['R'][2][2] == "YELLOW":
            print("found yellow edge on R")
            success = main_algorithm(cube,"D")
            edge_count, corner_count = count_yellow_pieces(cube)
            print(f"After main_algorithm: {edge_count} edges, {corner_count} corners")
            if success:
                print("🎉 Algorithm succeeded, stopping execution!")
                return

    '''
    ============================================================
         RUBIK'S CUBE - 2D UNFOLDED VIEW
============================================================

                           [ U ]
                              GREEN   YELLOW    GREEN
                               BLUE     BLUE     BLUE
                               BLUE     BLUE     BLUE

[ L ] [ F ] [ R ] [ B ]
  YELLOW   ORANGE   ORANGE    WHITE    WHITE    WHITE      RED      RED   YELLOW      RED    GREEN   ORANGE
  YELLOW   ORANGE   ORANGE    WHITE    WHITE    WHITE      RED      RED      RED   YELLOW   YELLOW     BLUE
    BLUE   ORANGE   ORANGE    WHITE    WHITE    WHITE      RED      RED     BLUE   YELLOW   YELLOW   YELLOW

                           [ D ]
                              GREEN    GREEN    GREEN
                              GREEN    GREEN    GREEN
                             ORANGE   ORANGE      RED
    Addt this test case
    '''
            
    if len(yellow_corners) == 2 and len(yellow_edges) == 4:
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
            edge_count, corner_count = count_yellow_pieces(cube)
            print(f"After main_algorithm: {edge_count} edges, {corner_count} corners")
            if success:
                print("🎉 Algorithm succeeded, stopping execution!")
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
            success = main_algorithm(cube, face_to_use)
            edge_count, corner_count = count_yellow_pieces(cube)
            print(f"After main_algorithm: {edge_count} edges, {corner_count} corners")
            if success:
                print("🎉 Algorithm succeeded, stopping execution!")
                return

        
        
        

    # Check for 2 adjacent yellow edges (like in side_algorithm)
    if len(yellow_edges) == 2:
        # Check if the 2 edges are adjacent (using same logic as side_algorithm)
        possible_adjacent_pairs = [[(0,1),(1,0)], [(0,1),(1,2)], [(1,0),(2,1)], [(1,2),(2,1)]]
        print("Hfedas")
        cube.visualize()
        for pair in possible_adjacent_pairs:
            if set(pair) == set(yellow_edges):
                print("Found 2 adjacent yellow edges - calling side_algorithm")
                print("RUNNING SIDE ALGORITHM")
                success = side_algorithm(cube)
                edge_count, corner_count = count_yellow_pieces(cube)
                print(f"After side_algorithm: {edge_count} edges, {corner_count} corners")
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
                print("SIDE ALGORITHM COMPLETED")
                
        
        # If we get here, the 2 edges are not adjacent
        print("Found 2 yellow edges but they are not adjacent")
    
    # Check for all 4 yellow edges with no yellow corners
    elif len(yellow_edges) == 4 and len(yellow_corners) == 0:
        print("Found all 4 yellow edges with no yellow corners - calling main_algorithm")
        success = main_algorithm(cube, "R")  # Pass random face "R"
        edge_count, corner_count = count_yellow_pieces(cube)
        print(f"After main_algorithm: {edge_count} edges, {corner_count} corners")
        if success:
            print("🎉 Algorithm succeeded, stopping execution!")
            return
        print("RUN MAIN ALGORITHM WITH RANDOM FACE ")
        
    
    # Check for all 4 yellow edges with exactly 1 yellow corner
    elif len(yellow_edges) == 4 and len(yellow_corners) == 1:
        print("FOUND 4 YELLOW EDGES WITH 1 YELLOW CORNER")
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
        print("INFO",info_corner)
        print("INFO",info_edge)
        cube.visualize()
        opposite_face = {"R":"L","L":"R","U":"D","D":"U"}
        if info_corner['face1'] == info_edge['face2']:
            face_to_use = info_corner['face1']
            print("FACE TO USE",face_to_use)
            cube.visualize()
            one_to_use = {"R":(2,2),"U":(0,2),"D":(2,0),"L":(0,0)}
            position_to_use = one_to_use.get(face_to_use)
            if cube.faces[face_to_use][position_to_use[0]][position_to_use[1]] == "YELLOW":
                print("or1:")
                cube.visualize()
                success = main_algorithm(cube, face_to_use)
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
            else:
                print("or2:")
                cube.visualize()
                success = main_algorithm(cube, face_to_use)
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
                success = main_algorithm(cube, opposite_face.get(face_to_use))
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
            edge_count, corner_count = count_yellow_pieces(cube)
            if edge_count!=3 and corner_count !=3:
                success = main_algorithm(cube, face_to_use)
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
            print("AFTER MAIN ALGORITHM")
            cube.visualize()
            print(f"After main_algorithm: {edge_count} edges, {corner_count} corners")
        elif info_corner['face2'] == info_edge['face2']:
            face_to_use = info_corner['face2']
            one_to_use = {"R":(2,2),"U":(0,2),"D":(2,0),"L":(0,0)}
            position_to_use = one_to_use.get(face_to_use)
            if cube.faces[face_to_use][position_to_use[0]][position_to_use[1]] == "YELLOW":
                print("or3:")
                success = main_algorithm(cube, face_to_use)
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
            else:
                print("or4:")
                success = main_algorithm(cube, face_to_use)
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
                success = main_algorithm(cube, opposite_face.get(face_to_use))
                if success:
                    print("🎉 Algorithm succeeded, stopping execution!")
                    return
            edge_count, corner_count = count_yellow_pieces(cube)
            print(f"After main_algorithm: {edge_count} edges, {corner_count} corners")
        else:
            raise ValueError("No matching pattern found")

    else:
        print(f"No matching pattern found - {len(yellow_edges)} edges, {len(yellow_corners)} corners")
    
    # Check if yellow face is completely solved (all 9 positions should be yellow)
    all_positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
    yellow_count = 0
    for pos in all_positions:
        if cube.faces['B'][pos[0]][pos[1]] == "YELLOW":
            yellow_count += 1
    
    if yellow_count == 9:
        print("🎉 Yellow face completely solved!")
    else:
        print(f"Yellow face not complete ({yellow_count}/9 yellow) - running solve_yellow again...")
        edge_count, corner_count = count_yellow_pieces(cube)
        print(f"After side_algorithm: {edge_count} edges, {corner_count} corners")
        print("in place of recursion")
        cube.visualize()
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


def side_algorithm(cube):
    #Do algorithm that is not really the main one but the one we use to use before the main one. 
    #We only call this when there is  at least three yellow edges on one side. In the format.
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
        
def solve_all_yellow_face(cube):
    """Solve the entire yellow face (both cross and corners)"""
    # First solve the yellow cross

    cube.visualize()
    print("FIRST RUN")
    solve_yellow(cube)
    cube.visualize()
    # cube.visualize()
    # print("SECOND RUN")
    # solve_yellow(cube)
    # cube.visualize()
    # print("THIRD RUN")
    #solve_yellow(cube)
    # cube.visualize()
    # print("FOURTH RUN")

    #test_pattern_recognition()



    
    # Then orient the yellow corners
    #solve_yellow_corners(cube)
    
    #print("Yellow face solving complete!")
    #controls.print_moves() 


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


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
        print(control)
        raise ValueError("Invalid control in run_control")

def solve_white_corner(cube, color1, color2, color3):
    color2face = {"RED": "R", "YELLOW": "B", "ORANGE": "L", "GREEN": "D", "BLUE": "U", "WHITE": "F"}
    info = cube.find_corner_with_colors(color1, color2, color3)

    if color2face.get(info['color1']) == info['face1'] and color2face.get(info['color2']) == info['face2'] and color2face.get(info['color3']) == info['face3']:
        print("✅Corner is in correct position")
        return;
    
    print("Solving white corner", color1, color2, color3)
    
    # Move WHITE to color3 if it's not already there
    if color1 == "WHITE":
        color1, color2, color3 = color2, color3, color1
    elif color2 == "WHITE":
        color1, color2, color3 = color1, color3, color2
    # If color3 == "WHITE", no swap needed
    info = cube.find_corner_with_colors(color1, color2, color3)

    # Fixed logic bug - determine alignment based on color combination
    if (color1 == "BLUE" and color2 == "ORANGE") or (color1 == "ORANGE" and color2 == "BLUE"):
        align_white = "ORANGE"
        align_other = "BLUE" # left
    elif (color1 == "BLUE" and color2 == "RED") or (color1 == "RED" and color2 == "BLUE"):
        align_white = "BLUE"
        align_other = "RED"
    elif (color1 == "RED" and color2 == "GREEN") or (color1 == "GREEN" and color2 == "RED"):
        align_white = "RED"
        align_other = "GREEN"
    elif (color1 == "GREEN" and color2 == "ORANGE") or (color1 == "ORANGE" and color2 == "GREEN"):
        align_white = "GREEN"
        align_other = "ORANGE"
    else:
        raise ValueError("Invalid colors for white corner")
    
    #CHECK IF ON LAYER 1 or 3
    layer1 = False
    layer3 = False
    if info['face1'] == 'F' or info['face2'] == 'F' or info['face3'] == 'F':
        layer1 = True
    else:
        layer3 = True
    if layer1:
        if color2face.get(info['color1']) == info['face1'] and color2face.get(info['color2']) == info['face2'] and color2face.get(info['color3']) == info['face3']:
            print("Corner is in correct position")
        else:
            left_dict = {'D':(0,0), 'U':(2,2), 'L':(0,2), 'R':(2,0)}
            right_dict = {'D':(0,2), 'U':(2,0), 'L':(2,2), 'R':(0,0)}
            right = False
            info = cube.find_corner_with_colors(color1, color2, color3)
            print(info['face1'])
            print("face1")
            #make sure to check if this is accurate, test for accuracy
            if info['position1'] == left_dict.get(info['face1']):
                right = False
                print("dis")
                print(info)
                print(color1, color2, color3)
            if info['position1'] == right_dict.get(info['face1']):
                right = True
                print("did")
            if info['face1'] == 'F':
                face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face2'], True)
            else:
                face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face1'], True)

            print("Face to flip", face_to_flip)
            if right:
                print("right")
                run_control(cube, face_to_flip, "clockwise")
                controls.B_prime(cube)
                run_control(cube, face_to_flip, "counterclockwise")
            else:
                print("left")
                cube.visualize()
                controls.print_moves()
                run_control(cube, face_to_flip, "clockwise")
                controls.B(cube)
                run_control(cube, face_to_flip, "counterclockwise")
                controls.print_moves()
                info2 = cube.find_corner_with_colors(color1, color2, color3)
                if info['corner_info'] == info2['corner_info']:
                    run_control(cube, face_to_flip, "clockwise")
                    controls.B_prime(cube)
                    run_control(cube, face_to_flip, "counterclockwise")
                    print("same")
                    controls.print_moves()
                    controls.moves_made.pop()
                    controls.moves_made.pop() 
                    controls.moves_made.pop()
                    controls.moves_made.pop()
                    controls.moves_made.pop()
                    controls.moves_made.pop()
                    controls.print_moves()
                    run_control(cube, face_to_flip, "counterclockwise")
                    controls.B(cube)
                    run_control(cube, face_to_flip, "clockwise") 
                    
    # This sums up the move from layer 1 to layer 3 if it is not in the right position from the start.
    
    #below happens regardless.
    info = cube.find_corner_with_colors(color1, color2, color3)
    if info['face1'] == 'F' or info['face2'] == 'F' or info['face3'] == 'F':
        print("❌❌❌❌ TRANSITION FAILED to layer 3")
    #here we should align the corner to the right position, then flip so that the white isn't on bottom.
    if info['face3'] == 'B':
        #PROBLEM HERE,NEED TO FIX ❌❌❌❌❌❌❌❌
        print("builtdif")
        (controls.print_moves())
        while not((info['face2'] == color2face.get(info['color2']) and info['face1'] == color2face.get(info['color1'])) or (info['face2'] == color2face.get(info['color1']) and info['face1'] == color2face.get(info['color2']))):
            controls.print_moves()
            print("aneiron")
            print(color1, color2, color3)
            controls.B(cube)
            info=cube.find_corner_with_colors(color1, color2, color3)
        (controls.print_moves())
        print("nah")
        print(info['face1'])
        info = cube.find_corner_with_colors(color1, color2, color3)
        face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face2'], True)
        right_dict = {'D':(2,2), 'U':(0,0), 'L':(2,0), 'R':(0,2)}
        if info['position1'] == right_dict.get(info['face1']):
            print("hah")
            run_control(cube, face_to_flip, "counterclockwise")
            controls.B_prime(cube)
            run_control(cube, face_to_flip, "clockwise")
        else:
            print("nah")
            run_control(cube, face_to_flip, "clockwise")
            controls.B(cube)
            run_control(cube, face_to_flip, "counterclockwise")
        # run_control(cube, face_to_flip, "counterclockwise")
        # controls.B_prime(cube)
        # run_control(cube, face_to_flip, "clockwise")
        controls.print_moves()
        print("fiasf")
    info = cube.find_corner_with_colors(color1, color2, color3)
    cube.visualize()
    print("Now we should have white not on bottom")
    controls.print_moves()
    if info['face3'] == 'B':
        print("❌❌❌❌ WHITE IS STILL ON BOTTOM")
    #now I need to align the corner to the right position, then flip the side that is not white and not on bottom.
    info = cube.find_corner_with_colors(color1, color2, color3)
    side_to_flip, color = (info['face1'], info['color1']) if info['face1'] != 'B' else (info['face2'], info['color2'])
    while(color2face.get(color) != info['face1'] and color2face.get(color) != info['face2']):
        controls.B(cube)
        info = cube.find_corner_with_colors(color1, color2, color3)
        #print(info)
    
        #now we perform either left or right move set to move corner to the right position
    info = cube.find_corner_with_colors(color1, color2, color3)
    right_dict = {'D':(2,2), 'U':(0,0), 'L':(2,0), 'R':(0,2)}
    left_dict = {'D':(0,0), 'U':(2,2), 'L':(0,2), 'R':(2,0)}
    face_to_use = info['face1'] if info['face1'] != 'B' else info['face2']
    if info['face1']!='B':
        print("nig1")
        #if face1 is not on B, then do this
        print(info)
        cube.visualize()
        if info['position3'] == right_dict.get(info['face3']):
            print("nig2")
            #if the position of face1 is on the right bottom corner, then do this
            cube.visualize()
            controls.B(cube)
            face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face1'], True)
            run_control(cube, face_to_flip, "counterclockwise")
            controls.B_prime(cube)
            run_control(cube, face_to_flip, "clockwise")
            cube.visualize()
            info = cube.find_corner_with_colors(color1, color2, color3)
        else:
            print("nig3")
            #if the position of face 1 is on the left bottom corner, then do this
            controls.print_moves()
            cube.visualize()
            controls.B_prime(cube)
            face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face1'], True)
            run_control(cube, face_to_flip, "clockwise")
            controls.B(cube)
            run_control(cube, face_to_flip, "counterclockwise")
    else:
        #if face2 is not on B, then do this
        if info['position3'] == right_dict.get(info['face3']):
            #if position2 is on the right bottom corner, then do this
            #WORKING
            print("nig4")
            cube.visualize()
            controls.B(cube)
            face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face2'], True)
            controls.print_moves()
            print("face to flip", face_to_flip)
            run_control(cube, face_to_flip, "counterclockwise")
            controls.B_prime(cube)
            run_control(cube, face_to_flip, "clockwise")
            cube.visualize()
            info = cube.find_corner_with_colors(color1, color2, color3)
        else:
            #if position2 is on the left bottom corner, then do this
            print("nig5")
            print(face_to_use)
            controls.print_moves()
            print(info)
            cube.visualize()
            controls.B_prime(cube)
            face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face2'], True)
            print("face to flip", face_to_flip)
            run_control(cube, face_to_flip, "clockwise")
            controls.B(cube)
            run_control(cube, face_to_flip, "counterclockwise")




    # if info['position1'] == right_dict.get(info['face1']):
    #     cube.visualize()
    #     controls.B(cube)
    #     face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face2'], True)
    #     run_control(cube, face_to_flip, "counterclockwise")
    #     controls.B_prime(cube)
    #     run_control(cube, face_to_flip, "clockwise")
    #     cube.visualize()
    #     info = cube.find_corner_with_colors(color1, color2, color3)
    # elif info['position2'] == left_dict.get(info['face2']):
    #     controls.B_prime(cube)
    #     face_to_flip, direction = cube.get_face_to_move_from_color_2(info['face2'], True)
    #     run_control(cube, face_to_flip, "clockwise")
    #     controls.B(cube)
    #     run_control(cube, face_to_flip, "counterclockwise")
    # print("nig")
    # controls.print_moves()
    # print(info)
    info = cube.find_corner_with_colors(color1, color2, color3)
    if color2face.get(info['color1']) == info['face1'] and color2face.get(info['color2']) == info['face2'] and color2face.get(info['color3']) == info['face3']:
        print("✅Corner is in correct position")
    else:
        print("❌Corner is not in correct position")







def solve_all_corners(cube):
    """Solve all 4 white corners"""
    solve_white_corner(cube, "RED", "GREEN", "WHITE")
    solve_white_corner(cube, "BLUE", "ORANGE", "WHITE")
    solve_white_corner(cube, "RED", "BLUE", "WHITE")
    solve_white_corner(cube, "GREEN", "ORANGE", "WHITE")







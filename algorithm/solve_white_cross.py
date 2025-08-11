import algorithm
import controls

#START OF FUNCTIONS
def run_control(cube, control, direction, do_not_append: bool = False):
    # Determine prime vs non-prime based on direction semantics used in this module
    is_prime = not (direction == "counterclockwise" or direction == "")
    move_str = f"{control}'" if is_prime else control

    if control == "U" :
        if not is_prime:
            controls.U(cube, do_not_append=do_not_append)
        else:
            controls.U_prime(cube, do_not_append=do_not_append)
    elif control == "D":
        if not is_prime:
            controls.D(cube, do_not_append=do_not_append)
        else:
            controls.D_prime(cube, do_not_append=do_not_append)
    elif control == "L":
        if not is_prime:
            controls.L(cube, do_not_append=do_not_append)
        else:
            controls.L_prime(cube, do_not_append=do_not_append)
    elif control == "R":
        if not is_prime:
            controls.R(cube, do_not_append=do_not_append)
        else:
            controls.R_prime(cube, do_not_append=do_not_append)
    elif control == "B":
        if not is_prime:
            controls.B(cube, do_not_append=do_not_append)
        else:
            controls.B_prime(cube, do_not_append=do_not_append)
    elif control == "F":
        if not is_prime:
            controls.F(cube, do_not_append=do_not_append)
        else:
            controls.F_prime(cube, do_not_append=do_not_append)
    else:
        raise ValueError("Invalid control in run_control")

    if do_not_append:
        return move_str
            
# Example: Find an edge
def solve_cubie(cube, color1, color2):
    if (cube.is_edge_in_correct_position(color1, color2)):
        return;
    if (color2 != "WHITE"):
        color1, color2 = color2, color1
    color2face = {"RED": "R", "YELLOW": "B", "ORANGE": "L", "GREEN": "D", "BLUE": "U", "WHITE": "F"}
    info = cube.find_edge_with_colors(color1, color2)
    listofMid = ["D","L","U","R"]
    if info['face2'] == 'F' or info['face1'] == 'F':
        print("JFDJ")
        if info['face1'] != color2face.get(color1) and info['face2'] == 'F':
            control, none = cube.get_face_to_move_from_color_2(info['face1'], True)
            print("dnjafs")
            print("arey1")
            run_control(cube, control,"")
            print(control,none)
            run_control(cube, control,"")
        elif info['face2'] != color2face.get(color2) and info['face1'] == 'F':
            print("dnjafs2")
            control, none = cube.get_face_to_move_from_color_2(info['face2'], True)
            print(control,none)
            print("arey2")
            run_control(cube, control,"")
            run_control(cube, control,"")
    info = cube.find_edge_with_colors(color1, color2)
    if (info['face1'] =='B' or info['face2'] =='B'):
        #print("hi1")
                #If one side of the cube is on the bottom face, then there is either one of two things we have to do.
                #1. If the non-white side is on the bottom face, then align it to the color before it and do a left rotation on that face then a right rotation on the face it is supposed to be on. Then undo the transformation done on the original face by doing a right rotation on the first face.
                #2. If the white side is on the bottom face, then align it to the right color, and then do two rotations on it to get it to the top face.
        if info['face1']!='B':
            #print("hi2")
            if color2face.get(color1)!=info['face1']:
                #print("hi3",color2face.get(color1),info['face1'])
                #print("INFO: ",info)
                while(color2face.get(color1)!=info['face1']):
                    #print("hi4",color2face.get(color1),info['face1'])
                    # control, none = cube.get_face_to_move_from_color_2(info['face2'], True)
                    # #print(control,none)
                    # run_control(control,"")
                    print("arey14")
                    controls.B(cube)
                    info = cube.find_edge_with_colors(color1, color2)
                    #print(color2face.get(color1),info['face1'])
            control, none = cube.get_face_to_move_from_color_2(info['face1'], True)
            print("arey3")
            run_control(cube, control,"")
            run_control(cube, control,"")
            info = cube.find_edge_with_colors(color1, color2)
            #print(info)
        else:
            #This is is the nonwhite side is on the bottom face
            #print("hii")
            if color2face.get(color1)!=info['face2']:
                #print("hii3:",color2face.get(color1))
                while(color2face.get(color1)!=info['face2']):
                    print("arey15")
                    controls.B(cube)
                    info = cube.find_edge_with_colors(color1, color2)
                print("arey16")
                controls.B(cube)
                info = cube.find_edge_with_colors(color1, color2)
                control, none = cube.get_face_to_move_from_color_2(info['face2'], True)
                temp = control
                print("arey4")
                print(color1,color2)
                controls.print_moves()
                run_control(cube, control,"")
                info = cube.find_edge_with_colors(color1, color2)
                control, none = cube.get_face_to_move_from_color_2(info['face1'], False)
                
                run_control(cube, control,"clockwise")
                run_control(cube, temp,"clockwise")
                controls.print_moves()
            else:
                print("arey17")
                controls.B(cube)
                info = cube.find_edge_with_colors(color1, color2)
                control, none = cube.get_face_to_move_from_color_2(info['face2'], True)
                temp = control
                print("arey5")
                run_control(cube, control,"")
                info = cube.find_edge_with_colors(color1, color2)
                control, none = cube.get_face_to_move_from_color_2(info['face1'], True)
                run_control(cube, control,"clockwise")
                run_control(cube, temp,"clockwise")
    elif (info['face1'] in listofMid and info['face2'] in listofMid):
        if info['face1'] == color2face.get(color1):
            if info['position1'] == (1,0):
                control, none = cube.get_face_to_move_from_color_2(info['face1'], False)
                print("arey18")
                print(control,none)
                run_control(cube, control,none)
                controls.print_moves()
            elif info['position1'] == (1,2):
                control, none = cube.get_face_to_move_from_color_2(info['face1'], False)
                print("arey19")
                run_control(cube, control,none)
            elif info['position1'] == (2,1):
                control, none = cube.get_face_to_move_from_color_2(info['face1'], False)  # False = clockwise
                print("arey6")
                run_control(cube, control, none)  # clockwise setup
                controls.B(cube)  # extract (direction doesn't matter for now)
                run_control(cube, control, "counterclockwise")  # undo with opposite
            elif info['position1'] == (0,1):
                cube.visualize()
                #raise ValueError("Invalid position for edge in middle layer")
                control, none = cube.get_face_to_move_from_color_2(info['face1'], True)
                run_control(cube, control, "counterclockwise")

            else:
                raise ValueError("Invalid position for edge in middle layer")
        else:
            #print("INFO:",info)
            if info['face1'] == 'L' or info['face1'] == 'R':
                if info['position1'] == (0,1):
                    control, none = cube.get_face_to_move_from_color_2(info['face1'], True)
                    print("arey7")
                    run_control(cube, control,none)
                    controls.B(cube)
                    run_control(cube, control,"clockwise")
                elif info['position1'] == (1,2):
                    #print("HITLER1")
                    control, none = cube.get_face_to_move_from_color_2(info['face1'], False)
                    print("arey8")
                    run_control(cube, control,none)
                    #print(control,none)
                    controls.B(cube)
                    run_control(cube, control,"counterclockwise")
                elif info['position1'] == (1,0):
                    control, none = cube.get_face_to_move_from_color_2(info['face1'], True)
                    print("arey9")
                    run_control(cube, control,none)
                    controls.B(cube) 
                    run_control(cube, control, "clockwise")
                elif info['position1'] == (2,1):
                    
                    control, none = cube.get_face_to_move_from_color_2(info['face1'], True)
                    print("arey10")
                    size = len(controls.moves_made)
                    temp_moves = []
                    temp_moves.append(run_control(cube, control,none, do_not_append=True))
                    temp_moves.append(run_control(cube, "B", "", do_not_append=True))
                    temp_moves.append(run_control(cube, control, "clockwise", do_not_append=True))
                    info2 = cube.find_edge_with_colors(color1, color2)
                    if info['edge_info'] == info2['edge_info']:
                        print("hiter")
                        temp_moves.append(run_control(cube, control, "counterclockwise", do_not_append=True))
                        temp_moves.append(run_control(cube, "B", "clockwise", do_not_append=True))
                        temp_moves.append(run_control(cube, control, "clockwise", do_not_append=True))
                        for move in temp_moves:
                            if move is not None:
                                controls.moves.append(move)
                                controls.moves_made.append(move)
                        run_control(cube, control,"clockwise")
                        controls.B(cube)
                        run_control(cube, control, "counterclockwise")
                        controls.print_moves()
                        print("duh")
                    else:
                        for move in temp_moves:
                            if move is not None:
                                controls.moves.append(move)
                                controls.moves_made.append(move)

                    controls.print_moves()
                else:
                    #print("hi3")
                    print("INFO:",info)
                    raise ValueError("Invalid position for edge in middle layer")
            else:
                if info['position2'] == (1,0):
                    #print("hi1")
                    control, none = cube.get_face_to_move_from_color_2(info['face2'], True)
                    print("arey11")
                    run_control(cube, control,none)
                    controls.B(cube)
                    run_control(cube, control,"clockwise")
                elif info['position2'] == (1,2):
                    #print("hi2")
                    control, none = cube.get_face_to_move_from_color_2(info['face2'], False)
                    print("arey12")
                    run_control(cube, control,none)
                    #print(control,none)
                    controls.B(cube)
                    run_control(cube, control,"counterclockwise")
                elif info['position2'] == (2,1):
                    control, none = cube.get_face_to_move_from_color_2(info['face2'], True)  # Like (1,0), not (1,2)
                    size = len(controls.moves_made)
                    print("arey13")
                    run_control(cube, control, none)
                    controls.B(cube)
                    run_control(cube, control, "clockwise")
                    controls.print_moves()
                    info2 = cube.find_edge_with_colors(color1, color2)
                    if info['edge_info'] == info2['edge_info']:
                        run_control(cube, control, "counterclockwise")
                        controls.B_prime(cube)
                        run_control(cube, control, "clockwise")
                        while(len(controls.moves_made) > size):
                            print("poppy2")
                            controls.moves_made.pop()
                        run_control(cube, control,"clockwise")
                        controls.B(cube)
                        run_control(cube, control, "counterclockwise")
                        controls.print_moves()
                        print("duh")

                    controls.print_moves()
                elif (info['position2'] == (0,1) and info['face2'] == 'R'):
                    print("hi2")
                    controls.print_moves()
                    control, none = cube.get_face_to_move_from_color_2(info['face1'], True)  # Like (1,0), not (1,2)
                    print("arey20")
                    run_control(cube, control, none)
                    print("arey21")
                    controls.B(cube)
                    print("arey22")
                    run_control(cube, control, "clockwise")
                    controls.print_moves()
                    print("hi3")
                elif (info['position2'] == (0,1) and info['face2'] == 'L'):
                    print("hi2")
                    controls.print_moves()
                    control, none = cube.get_face_to_move_from_color_2(info['face1'], False)  # Like (1,0), not (1,2)
                    print("arey20")
                    run_control(cube, control, none)
                    print("arey21")
                    controls.B(cube)
                    print("arey22")
                    run_control(cube, control, "counterclockwise")
                    controls.print_moves()
                    print("hi3")
                else:
                    #print("hi3")
                    print("INFO:",info)
                    cube.visualize()
                    print(info)
                    raise ValueError("Invalid position for edge in middle layer")
            controls.print_moves()
            cube.visualize()
            solve_cubie(cube, color1, color2)

def solve_all_edges(cube):
    """Solve all 4 white cross edges"""
    controls.print_moves()
    solve_cubie(cube, "WHITE", "BLUE")
    controls.print_moves()
    solve_cubie(cube, "WHITE", "RED")
    solve_cubie(cube, "WHITE", "ORANGE")
    solve_cubie(cube, "WHITE", "GREEN")
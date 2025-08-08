import algorithm
import controls


def run_control(cube, control, direction):
    """Dispatch a single face turn to the appropriate control function.

    control: one of "U", "D", "L", "R", "B", "F"
    direction: "counterclockwise" or "clockwise" ("" treated as counterclockwise)
    """
    if control == "U":
        if direction == "counterclockwise" or direction == "":
            controls.U(cube)
        else:
            controls.U_prime(cube)
    elif control == "D":
        if direction == "counterclockwise" or direction == "":
            controls.D(cube)
        else:
            controls.D_prime(cube)
    elif control == "L":
        if direction == "counterclockwise" or direction == "":
            controls.L(cube)
        else:
            controls.L_prime(cube)
    elif control == "R":
        if direction == "counterclockwise" or direction == "":
            controls.R(cube)
        else:
            controls.R_prime(cube)
    elif control == "B":
        if direction == "counterclockwise" or direction == "":
            controls.B(cube)
        else:
            controls.B_prime(cube)
    elif control == "F":
        if direction == "counterclockwise" or direction == "":
            controls.F(cube)
        else:
            controls.F_prime(cube)
    else:
        raise ValueError("Invalid control in run_control")








def first_algorithm(cube, face):
    #face is the one that is the marker
    """First algorithm placeholder for the last stage."""
    controls.print_moves()
    opposite_face = {"R":"L","L":"R","U":"D","D":"U"}
    center = opposite_face.get(face)
    reverse_on_right = {"D":"L","R":"D","U":"R","L":"U"}
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(center), True)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(center, False)
    run_control(cube, control, direction)
    print(control, direction)
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(center), True)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(face, False)
    run_control(cube, control, direction)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(center), False)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(center, True)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(center), True)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(face, False)
    run_control(cube, control, direction)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(center), False)
    run_control(cube, control, direction)
    run_control(cube, control, direction)
    controls.B(cube)
    controls.print_moves()
    pass


def final_algorithm(cube, face):
    #face is the one that has one full complete side. NOT WHITE.
    """Final algorithm placeholder for the last stage."""
    opposite_face = {"R":"L","L":"R","U":"D","D":"U"}
    center = opposite_face.get(face)
    reverse_on_right = {"D":"L","R":"D","U":"R","L":"U"}
    reverse_on_left = {"D":"R","L":"D","U":"L","R":"U"}
    controls.print_moves()

    control, direction = cube.get_face_to_move_from_color_2(center, False)
    run_control(cube, control, direction)
    run_control(cube, control, direction)
    controls.B_prime(cube)
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_left.get(center), False)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(center), True)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(center, False)
    run_control(cube, control, direction)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_left.get(center), True)
    run_control(cube, control, direction)
    control, direction = cube.get_face_to_move_from_color_2(reverse_on_right.get(center), False)
    run_control(cube, control, direction)
    controls.B_prime(cube)
    control, direction = cube.get_face_to_move_from_color_2(center, True)
    run_control(cube, control, direction)
    run_control(cube, control, direction)
    controls.print_moves()




    pass


def solve(cube):
    #call final and first algorithm in their appropriate order.
    cube.visualize()
    #first_algorithm(cube, "U")
    controls.B(cube)
    cube.visualize()
    final_algorithm(cube, "L")
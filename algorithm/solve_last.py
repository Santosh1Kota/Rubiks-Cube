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
    print("first algorithm:", face)
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
    # After running the first algorithm, align any existing bar with its face color.
    # Safe if no bar exists (function returns False and does nothing).
    align_bars_with_face_colors(cube, prefer_face=face)
    pass


def final_algorithm(cube, face):
    print("final algorithm:", face)
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


def check_b_corner_bars(cube):
    """Check U, D, L, R faces for a 'bar' on corners touching B.

    For each face among U, D, L, R, we look at the two corner stickers that
    touch the B layer, and check if those two stickers on that face are the
    same color (non-WHITE) AND the middle sticker between them is a different color.

    Returns:
    - "none" if no faces have the pattern
    - the face name (e.g., "U") if exactly one face has the pattern
    - "all" if all four faces have the pattern
    - "multiple" if 2 or 3 faces have the pattern (tell me if you want a different behavior)
    """
    faces_to_check = ["U", "D", "L", "R"]
    # Positions (row, col) on each face that touch B corners
    positions_by_face = {
        "U": [(0, 0), (0, 2)],
        "D": [(2, 0), (2, 2)],
        "R": [(0, 2), (2, 2)],
        "L": [(0, 0), (2, 0)],
    }
    # Middle positions between the two corners on each face
    middle_by_face = {
        "U": (0, 1),
        "D": (2, 1),
        "R": (1, 2),
        "L": (1, 0),
    }

    faces_with_bar = []

    for face in faces_to_check:
        (row1, col1), (row2, col2) = positions_by_face[face]
        color_one = cube.faces[face][row1][col1]
        color_two = cube.faces[face][row2][col2]
        mid_r, mid_c = middle_by_face[face]
        middle_color = cube.faces[face][mid_r][mid_c]

        # corners equal and non-WHITE, and middle is a different color
        if color_one == color_two and color_one != "WHITE" and middle_color != color_one:
            faces_with_bar.append(face)

    if not faces_with_bar:
        return "none"
    if len(faces_with_bar) == 4:
        return "all"
    if len(faces_with_bar) == 1:
        return faces_with_bar[0]

    # 2 or 3 faces match; let me know if you prefer a different return
    return "multiple"


def get_b_corner_bar_faces(cube):
    """Return U/D/L/R faces that have the B-corner bar pattern.

    Pattern: the two B-touching corner stickers on the face are equal and non-WHITE,
    and the middle sticker between them is a different color.
    """
    faces_to_check = ["U", "D", "L", "R"]
    positions_by_face = {
        "U": [(0, 0), (0, 2)],
        "D": [(2, 0), (2, 2)],
        "R": [(0, 2), (2, 2)],
        "L": [(0, 0), (2, 0)],
    }
    middle_by_face = {
        "U": (0, 1),
        "D": (2, 1),
        "R": (1, 2),
        "L": (1, 0),
    }

    faces_with_bar = []
    for face in faces_to_check:
        (row1, col1), (row2, col2) = positions_by_face[face]
        color_one = cube.faces[face][row1][col1]
        color_two = cube.faces[face][row2][col2]
        mid_r, mid_c = middle_by_face[face]
        middle_color = cube.faces[face][mid_r][mid_c]
        if color_one == color_two and color_one != "WHITE" and middle_color != color_one:
            faces_with_bar.append(face)
    return faces_with_bar


def is_face_complete(cube, face):
    """Return True if the entire 3x3 face matches its center color."""
    center_color = cube.faces[face][1][1]
    for r in range(3):
        for c in range(3):
            if cube.faces[face][r][c] != center_color:
                return False
    return True


def get_complete_faces(cube):
    """Return a list of faces among U, D, L, R that are fully complete."""
    faces_to_check = ["U", "D", "L", "R"]
    return [face for face in faces_to_check if is_face_complete(cube, face)]


def detect_three_bars_one_complete(cube):
    """Detect the case: exactly three bar-pattern faces and exactly one complete face.

    Returns the name of the complete face if detected, otherwise "none".
    """
    bar_faces = get_b_corner_bar_faces(cube)
    complete_faces = get_complete_faces(cube)

    if len(bar_faces) == 3 and len(complete_faces) == 1:
        return complete_faces[0]
    return "none"


def _bar_corners_match_center(cube, face):
    """Return True if the B-touching corner pair on `face` equals the face center color.

    Requires that the face currently has a bar by our definition (we don't enforce that here).
    """
    positions_by_face = {
        "U": [(0, 0), (0, 2)],
        "D": [(2, 0), (2, 2)],
        "R": [(0, 2), (2, 2)],
        "L": [(0, 0), (2, 0)],
    }
    (r1, c1), (r2, c2) = positions_by_face[face]
    corner_color = cube.faces[face][r1][c1]
    center_color = cube.faces[face][1][1]
    return corner_color == center_color


def align_bars_with_face_colors(cube, prefer_face=None):
    """If there is at least one bar, rotate B until a chosen bar's color matches its face center.

    - If `prefer_face` is provided and currently has a bar, try to align that face.
    - Otherwise, use the first face from `get_b_corner_bar_faces(cube)`.
    - Up to 4 B rotations are attempted.

    Returns True if alignment achieved for the chosen face, False otherwise.
    """
    attempts = 0
    while attempts < 4:
        bar_faces = get_b_corner_bar_faces(cube)
        if not bar_faces:
            return False
        face_to_align = prefer_face if (prefer_face in bar_faces) else bar_faces[0]
        if _bar_corners_match_center(cube, face_to_align):
            return True
        # rotate B and retry
        controls.B(cube)
        attempts += 1
    # Final check after 4 rotations
    bar_faces = get_b_corner_bar_faces(cube)
    if not bar_faces:
        return False
    face_to_align = prefer_face if (prefer_face in bar_faces) else bar_faces[0]
    return _bar_corners_match_center(cube, face_to_align)


def solve(cube, depth: int = 0, max_depth: int = 20):
    '''
    FIRST: If there are no bar patterns on U/D/L/R, run the first algorithm and re-check.
    SECOND: If there is exactly one bar, align that face so the bar color matches the face center,
            then run the first algorithm on that face; re-check.
    THIRD: If there are bars on all four faces and no complete face, run the final algorithm on any face; re-check.
    FOURTH: If exactly one complete face exists and the other three faces have the bar pattern,
            run the final algorithm on that complete face; re-check.
    '''
    # Base conditions
    if cube.is_solved():
        print("solved")
        return True
    if depth >= max_depth:
        print("max depth reached")
        raise Exception("Max depth reached")

    bar_faces = get_b_corner_bar_faces(cube)
    complete_faces = get_complete_faces(cube)

    # FOURTH: 3 bars + 1 complete face → final on complete face
    if len(bar_faces) == 3 and len(complete_faces) == 1:
        print("first")
        cube.visualize()
        final_algorithm(cube, complete_faces[0])
        print("after")
        cube.visualize()
        return solve(cube, depth + 1, max_depth)

    # THIRD: 4 bars and 0 complete faces → final on any face (use U)
    if len(bar_faces) == 4 and len(complete_faces) == 0:
        print("second")
        cube.visualize()
        align_bars_with_face_colors(cube)
        final_algorithm(cube, "U")
        print("after")
        cube.visualize()
        return solve(cube, depth + 1, max_depth)

    # SECOND: exactly 1 bar → align that face then run first algorithm on it
    if len(bar_faces) == 1:
        print("third")
        cube.visualize()
        face = bar_faces[0]
        align_bars_with_face_colors(cube, prefer_face=face)
        first_algorithm(cube, face)
        print("after")
        cube.visualize()
        return solve(cube, depth + 1, max_depth)

    # FIRST: no bars → run first algorithm on a default face (U)
    if len(bar_faces) == 0:
        print("fourth")
        cube.visualize()
        first_algorithm(cube, "U")
        print("after")
        cube.visualize()
        return solve(cube, depth + 1, max_depth)

    # Fallback: 2 or 3 bars, but not the 3-bars + 1-complete case
    # Heuristic: align one bar and run first algorithm there
    face = bar_faces[0]
    align_bars_with_face_colors(cube, prefer_face=face)
    first_algorithm(cube, face)
    
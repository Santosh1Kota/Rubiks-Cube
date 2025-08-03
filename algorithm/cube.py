import numpy as np
import random
from cubie import Cubie  # Make sure Cubie uses tuples for positions and face_colors keys

class RubiksCube:
    FACE_NORMALS = {
        'f': (0, 0, 1),
        'b': (0, 0, -1),
        'u': (0, 1, 0),
        'd': (0, -1, 0),
        'l': (-1, 0, 0),
        'r': (1, 0, 0)
    }

    FACE_TO_COORD_FUNC = {
        'f': lambda i, j: (j - 1, 1 - i, 1),
        'b': lambda i, j: (1 - j, 1 - i, -1),
        'u': lambda i, j: (j - 1, 1, -(i - 1)),
        'd': lambda i, j: (j - 1, -1, i - 1),
        'l': lambda i, j: (-1, 1 - i, -(j - 1)),
        'r': lambda i, j: (1, 1 - i, j - 1)
    }

    FACE_TO_AXIS = {
        'f': 'z',
        'b': 'z',
        'u': 'y',
        'd': 'y',
        'l': 'x',
        'r': 'x'
    }

    FACE_NORMAL_TO_VALUE = {
        'f': 1,
        'b': -1,
        'u': 1,
        'd': -1,
        'l': -1,
        'r': 1
    }

    def __init__(self, cube_state):
        self.cubies = {}

        for face, grid in cube_state.items():
            normal = self.FACE_NORMALS[face]
            coord_func = self.FACE_TO_COORD_FUNC[face]

            for i in range(3):
                for j in range(3):
                    color = grid[i][j]
                    pos = coord_func(i, j)

                    if pos not in self.cubies:
                        self.cubies[pos] = Cubie(position=pos, face_colors={})
                    self.cubies[pos].face_colors[normal] = color

    def get_cubies(self):
        return list(self.cubies.values())

    def print_cube(self):
        for pos, cubie in sorted(self.cubies.items()):
            print(f"Pos: {pos}, Faces: {cubie.face_colors}")

    def rotate(self, moves):
        if isinstance(moves, str):
            moves = moves.split()  # handles "R U R' U'" input

        for move in moves:
            if move[-1] == "'":  # counterclockwise
                face = move[0].lower()
                clockwise = False
            else:
                face = move.lower()
                clockwise = True
            self.rotate_face(face, clockwise)

    def rotate_face(self, face, clockwise):
        axis = self.FACE_TO_AXIS[face]
        normal = self.FACE_NORMALS[face]
        layer_coord = self.FACE_NORMAL_TO_VALUE[face]

        affected = [
            cubie for pos, cubie in self.cubies.items()
            if pos['xyz'.index(axis)] == layer_coord
        ]

        updates = {}

        for cubie in affected:
            old_pos = tuple(cubie.position)
            new_pos = tuple(self.rotate_vector(old_pos, axis, clockwise))

            new_face_colors = {
                tuple(self.rotate_vector(n, axis, clockwise)): c
                for n, c in cubie.face_colors.items()
            }

            cubie.position = new_pos
            cubie.face_colors = new_face_colors
            updates[new_pos] = cubie

            del self.cubies[old_pos]

        self.cubies.update(updates)

    @staticmethod
    def rotate_vector(vec, axis, clockwise=True):
        x, y, z = vec
        if axis == 'x':
            return (x, -z, y) if clockwise else (x, z, -y)
        elif axis == 'y':
            return (z, y, -x) if clockwise else (-z, y, x)
        elif axis == 'z':
            return (-y, x, z) if clockwise else (y, -x, z)

    def is_solved(self):
        face_colors = {face: set() for face in self.FACE_NORMALS}
        for cubie in self.cubies.values():
            for normal, color in cubie.face_colors.items():
                face = [k for k, v in self.FACE_NORMALS.items() if v == normal][0]
                face_colors[face].add(color)
        return all(len(colors) == 1 for colors in face_colors.values())

    def scramble(self, num_moves=20):
        moves = ["f", "b", "u", "d", "l", "r", "f'", "b'", "u'", "d'", "l'", "r'"]
        scramble_seq = [random.choice(moves) for _ in range(num_moves)]
        self.rotate(scramble_seq)
        return scramble_seq


# === DEMO ===
if __name__ == '__main__':
    cube_state = {
        'f': [['red'] * 3 for _ in range(3)],
        'b': [['orange'] * 3 for _ in range(3)],
        'u': [['white'] * 3 for _ in range(3)],
        'd': [['yellow'] * 3 for _ in range(3)],
        'l': [['green'] * 3 for _ in range(3)],
        'r': [['blue'] * 3 for _ in range(3)],
    }

    cube = RubiksCube(cube_state)

    print("=== Before Scramble ===")
    cube.print_cube()
    print("\nIs Solved:", cube.is_solved())

    scramble_moves = cube.scramble(10)
    print("\n-- Scrambled with moves --")
    print("Scramble:", ' '.join(scramble_moves))
    print("Is Solved:", cube.is_solved())

    # Solve by reversing
    solution_moves = []
    for m in reversed(scramble_moves):
        solution_moves.append(m[:-1] if m.endswith("'") else m + "'")

    cube.rotate(solution_moves)
    print("\n-- After Solving --")
    cube.print_cube()
    print("Is Solved:", cube.is_solved())
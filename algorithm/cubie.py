import numpy as np

class Cubie:
    def __init__(self, position, face_colors):
        self.position = np.array(position)
        self.face_colors = face_colors  # Dict: direction vector -> color
    def z90(self, direction):
        if direction == "clockwise":
            Rz = np.array([
                [0, -1, 0],
                [1,  0, 0],
                [0,  0, 1]
            ])
        else:
            Rz = np.array([
                [0, 1, 0],
                [-1, 0, 0],
                [0, 0, 1]
            ])
        self.position = Rz @ self.position
        new_face_colors = {}
        for face_dir, color in self.face_colors.items():
            new_dir = Rz @ np.array(face_dir)
            new_face_colors[tuple(int(x) for x in new_dir)] = color
        self.face_colors = new_face_colors
    def x90(self, direction):
        if direction == "clockwise":
            Rx = np.array([
            [1,  0,  0],
            [0,  0, -1],
            [0,  1,  0]
            ])
        else:
            Rx = np.array([
            [1,  0,  0],
            [0,  0,  1],
            [0, -1,  0]
            ])
        self.position = Rx @ self.position
        new_face_colors = {}
        for face_dir, color in self.face_colors.items():
            new_dir = Rx @ np.array(face_dir)
            new_face_colors[tuple(int(x) for x in new_dir)] = color
        self.face_colors = new_face_colors
    
    def y90(self,direction):
        if direction == "clockwise":
            Ry = np.array([
            [0,  0,  1],
            [0,  1, 0],
            [-1,  0,  0]
            ])
        else:
            Ry = np.array([
            [0,  0,  -1],
            [0,  1, 0],
            [1,  0,  0]
            ])
        self.position = Ry @ self.position
        new_face_colors = {}
        for face_dir, color in self.face_colors.items():
            new_dir = Ry @ np.array(face_dir)
            new_face_colors[tuple(int(x) for x in new_dir)] = color
        self.face_colors = new_face_colors



c = Cubie(
    position=(1, 1, 1),
    face_colors={
        (1, 0, 0): 'red',
        (0, 1, 0): 'white',
        (0, 0, 1): 'blue'
    }
)
print("Before:")
print("Position:", c.position)
print("Face colors:", c.face_colors)

c.z90("clockwise")

print("\nAfter Z 90° CW rotation:")
print("Position:", c.position)
print("Face colors:", c.face_colors)

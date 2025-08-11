import controls

class RubiksCube:
    def __init__(self, filename):
        self.faces = {
            'U': [['' for _ in range(3)] for _ in range(3)],
            'F': [['' for _ in range(3)] for _ in range(3)],
            'R': [['' for _ in range(3)] for _ in range(3)],
            'L': [['' for _ in range(3)] for _ in range(3)],
            'B': [['' for _ in range(3)] for _ in range(3)],
            'D': [['' for _ in range(3)] for _ in range(3)],
        }
        self.move_log = []  # Track all moves made (in standard notation)
        self.step_log = []  # Track solving steps
        self.logging_enabled = True  # Control whether moves are logged
        self.quiet_mode = False  # Control output verbosity
        self.load_from_file(filename)
    
    def log_move(self, move):
        """Log a single move in standard Rubik's cube notation."""
        if self.logging_enabled:
            self.move_log.append(move)
            if not self.quiet_mode:
                print(f"🔄 Move {len(self.move_log)}: {move}")
    
    def log_step(self, step_name, moves):
        """Log a solving step with its moves."""
        self.step_log.append({
            'step': step_name,
            'moves': moves,
            'move_count': len(moves)
        })
        print(f"📝 Logged step: {step_name} - {len(moves)} moves")
    
    def get_total_moves(self):
        """Get the total number of moves made so far."""
        return len(self.move_log)
    
    def get_all_moves(self):
        """Get all moves made so far in standard notation."""
        return self.move_log.copy()
    
    def get_move_sequence_string(self):
        """Get all moves as a single string for easy replay."""
        return ' '.join(self.move_log)
    
    def save_moves_to_file(self, filename):
        """Save all moves to a text file for replay."""
        with open(filename, 'w') as f:
            f.write(self.get_move_sequence_string())
        print(f"💾 Saved {len(self.move_log)} moves to {filename}")
    
    def get_move_summary(self):
        """Get a summary of all moves made."""
        if not self.step_log:
            return "No moves logged yet."
        
        summary = []
        summary.append("="*60)
        summary.append("         COMPLETE MOVE LOG")
        summary.append("="*60)
        
        total_moves = 0
        for i, step in enumerate(self.step_log, 1):
            summary.append(f"\n{i}. {step['step']}: {step['move_count']} moves")
            if step['moves']:
                summary.append(f"   Moves: {' '.join(step['moves'])}")
            total_moves += step['move_count']
        
        summary.append(f"\n📊 TOTAL MOVES: {total_moves}")
        summary.append(f"🎯 FULL SEQUENCE: {' '.join(self.move_log)}")
        summary.append("="*60)
        
        return "\n".join(summary)
    
    def clear_logs(self):
        """Clear all move and step logs."""
        self.move_log = []
        self.step_log = []
        print("🧹 Cleared all move logs")

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                tokens = line.strip().split()
                face = tokens[0]
                colors = tokens[1:]
                for i in range(9):
                    self.faces[face][i // 3][i % 3] = colors[i]
        
        
        # Apply transformations to the loaded data
        self.apply_source_transformations()

    def apply_source_transformations(self):
        """Apply transformations to the source data in self.faces"""
        # Transform U and D faces: flip rows (3→1)
        for face in ['U', 'D']:
            self.faces[face] = self.faces[face][::-1]
        
        # Transform L and R faces: flip columns within each row
        for face in ['L', 'R']:
            self.faces[face] = [row[::-1] for row in self.faces[face]]
        
        # Swap U and D faces
        self.faces['U'], self.faces['D'] = self.faces['D'], self.faces['U']

    def display(self):
        # Optional utility to print the cube
        for face in ['U', 'F', 'R', 'L', 'B', 'D']:
            print(f"{face}:")
            for row in self.faces[face]:
                print(" ".join(row))
            print()

    def is_solved(self) -> bool:
        """Return True if the cube is solved: every face is uniform.

        A face is considered solved when all 9 stickers match that face's center color.
        """
        for face in ['U', 'F', 'R', 'L', 'B', 'D']:
            center_color = self.faces[face][1][1]
            for row in range(3):
                for col in range(3):
                    if self.faces[face][row][col] != center_color:
                        return False
        return True

    
    def visualize(self):
        """
         Print the cube in 2D unfolded view:
               [ U ]
         [ L ] [ F ] [ R ] [ B ]
               [ D ]
         """
        def format_face(face_grid):
            return [" ".join(f"{color:>8}" for color in row) for row in face_grid]

        # Format all faces (transformations already applied in source data)
        faces_formatted = {}
        for face in ['U', 'F', 'R', 'L', 'B', 'D']:
            faces_formatted[face] = format_face(self.faces[face])

        # Print
        face_width = len(faces_formatted['F'][0])
        pad = " " * (face_width + 1)

        print("\n" + "="*60)
        print("         RUBIK'S CUBE - 2D UNFOLDED VIEW")
        print("="*60)

        # Top (U face)
        print(f"\n{pad}[ U ]")
        for row in faces_formatted['U']:
            print(f"{pad}{row}")

        # Middle (L F R B)
        print(f"\n[ L ] [ F ] [ R ] [ B ]")
        for i in range(3):
            line = f"{faces_formatted['L'][i]} {faces_formatted['F'][i]} {faces_formatted['R'][i]} {faces_formatted['B'][i]}"
            print(line)

        # Bottom (D face)
        print(f"\n{pad}[ D ]")
        for row in faces_formatted['D']:
            print(f"{pad}{row}")

        print("\n" + "="*60 + "\n")

    # --- Beginner Method Solving Steps ---
    def is_edge_in_correct_position(self, color1, color2):
        """Checks if the edge is in the right spot and orientation."""
        # First, determine what the center colors are for each face
        centers = {
            'U': self.faces['U'][1][1],
            'F': self.faces['F'][1][1], 
            'R': self.faces['R'][1][1],
            'L': self.faces['L'][1][1],
            'B': self.faces['B'][1][1],
            'D': self.faces['D'][1][1]
        }
        
        # Find which face has WHITE as its center (this is our "white cross" face)
        white_face = None
        for face, center_color in centers.items():
            if center_color == "WHITE":
                white_face = face
                break
        
        if white_face is None:
            return False
        
        # For white cross, we want WHITE on the white center face and the other color on its corresponding face
        if color1 == "WHITE":
            white_color = color1
            other_color = color2
        elif color2 == "WHITE":
            white_color = color2
            other_color = color1
        else:
            # For middle layer edges, use the middle layer checker
            return self.is_middle_edge_in_correct_position(color1, color2)
        
        # Find which face has the other_color as its center
        target_face = None
        for face, center_color in centers.items():
            if center_color == other_color:
                target_face = face
                break
        
        if target_face is None:
            return False
        
        # Define the correct edge positions based on white face and target face
        # We need to find the edge between white_face and target_face
        edge_map = {
            # Format: (face1, row1, col1, face2, row2, col2)
            ('U', 'F'): ('U', 2, 1, 'F', 0, 1),
            ('U', 'R'): ('U', 1, 2, 'R', 0, 1),
            ('U', 'B'): ('U', 0, 1, 'B', 0, 1),
            ('U', 'L'): ('U', 1, 0, 'L', 0, 1),
            ('F', 'R'): ('F', 1, 2, 'R', 1, 0),
            ('F', 'D'): ('F', 2, 1, 'D', 0, 1),
            ('F', 'L'): ('F', 1, 0, 'L', 1, 2),
            ('R', 'B'): ('R', 1, 2, 'B', 1, 0),
            ('R', 'D'): ('R', 2, 1, 'D', 1, 2),
            ('B', 'L'): ('B', 1, 2, 'L', 1, 0),
            ('B', 'D'): ('B', 2, 1, 'D', 2, 1),
            ('L', 'D'): ('L', 2, 1, 'D', 1, 0),
        }
        
        # Find the edge between white_face and target_face
        edge_key = (white_face, target_face) if (white_face, target_face) in edge_map else (target_face, white_face)
        
        if edge_key not in edge_map:
            return False
        
        # Get the correct edge position
        face1, r1, c1, face2, r2, c2 = edge_map[edge_key]
        
        # Check if the edge is in the correct position with correct orientation
        color_on_face1 = self.faces[face1][r1][c1]
        color_on_face2 = self.faces[face2][r2][c2]
        
        # Check if WHITE is on white_face and other color is on target_face
        if face1 == white_face and face2 == target_face:
            return (color_on_face1 == white_color and color_on_face2 == other_color)
        elif face1 == target_face and face2 == white_face:
            return (color_on_face1 == other_color and color_on_face2 == white_color)
        else:
            return False

    def is_middle_edge_in_correct_position(self, color1, color2):
        """Checks if a middle layer edge is in the correct position."""
        # Use the same color mapping as in solve_middle_layer.py
        color2face = {"RED": "R", "YELLOW": "B", "ORANGE": "L", "GREEN": "D", "BLUE": "U", "WHITE": "F"}
        
        # Find which faces have these colors
        face1 = color2face.get(color1)
        face2 = color2face.get(color2)
        
        if face1 is None or face2 is None:
            return False
        
        # Middle layer edge positions (excluding WHITE-F and YELLOW-B faces)
        middle_edge_map = {
            ('U', 'R'): ('U', 1, 2, 'R', 0, 1),  # U-R edge (BLUE-RED)
            ('U', 'L'): ('U', 1, 0, 'L', 0, 1),  # U-L edge (BLUE-ORANGE)  
            ('L', 'D'): ('L', 2, 1, 'D', 1, 0),  # L-D edge (ORANGE-GREEN)
            ('R', 'D'): ('R', 2, 1, 'D', 1, 2),  # R-D edge (RED-GREEN)
        }
        
        # Find the edge between face1 and face2
        edge_key = (face1, face2) if (face1, face2) in middle_edge_map else (face2, face1)
        
        if edge_key not in middle_edge_map:
            return False
        
        # Get the correct edge position
        f1, r1, c1, f2, r2, c2 = middle_edge_map[edge_key]
        
        # Check if colors are in correct positions
        color_on_f1 = self.faces[f1][r1][c1]
        color_on_f2 = self.faces[f2][r2][c2]
        
        # Check both orientations
        if f1 == face1 and f2 == face2:
            return (color_on_f1 == color1 and color_on_f2 == color2)
        elif f1 == face2 and f2 == face1:
            return (color_on_f1 == color2 and color_on_f2 == color1)
        else:
            return False


    def get_face_to_move_from_color_2(self, face, isLeft):
        #only for one specific case of the cubie being on the middle layer. The layer between white and yellow faces.
        #This function gives the move/control that gets the cubie to the white face if its in the center. If its left, then it should be clockwise, if is right, it should be counterclockwise. 
        #create a dictionary that links face rotated to the control based on looking at controls.
        face2control = {"L":"U","R":"D","D":"L","U":"R","B":"B","F":"F"}
        control = face2control.get(face)
        if isLeft:
            return (control,"counterclockwise")
        else:
            return (control,"clockwise")
    
    
    def _is_white_cross_solved(self):
        """Check if the white cross is completely solved."""
        target_pairs = [("WHITE", "RED"), ("WHITE", "BLUE"), ("WHITE", "ORANGE"), ("WHITE", "GREEN")]
        
        for color1, color2 in target_pairs:
            if not self.is_edge_in_correct_position(color1, color2):
                return False
        
        return True

    def _is_white_corners_solved(self):
        """Check if all white corners are completely solved."""
        color2face = {"RED": "R", "YELLOW": "B", "ORANGE": "L", "GREEN": "D", "BLUE": "U", "WHITE": "F"}
        target_corners = [
            ("RED", "GREEN", "WHITE"),
            ("BLUE", "ORANGE", "WHITE"), 
            ("RED", "BLUE", "WHITE"),
            ("GREEN", "ORANGE", "WHITE")
        ]
        
        for color1, color2, color3 in target_corners:
            info = self.find_corner_with_colors(color1, color2, color3)
            if info is None:
                return False
            
            # Check if each color is on its corresponding face
            if not (color2face.get(info['color1']) == info['face1'] and 
                   color2face.get(info['color2']) == info['face2'] and 
                   color2face.get(info['color3']) == info['face3']):
                return False
        
        return True

    def is_yellow_face_solved(self) -> bool:
        """Return True if the yellow face (B) is fully yellow (all 9 stickers)."""
        face_grid = self.faces['B']
        for row in range(3):
            for col in range(3):
                if face_grid[row][col] != "YELLOW":
                    return False
        return True

    def is_middle_edges_solved(self) -> bool:
        """Return True if all four middle-layer edges are in correct positions and orientations.

        Uses the same color-face mapping and validation as is_middle_edge_in_correct_position.
        Target pairs: (BLUE, RED), (BLUE, ORANGE), (ORANGE, GREEN), (RED, GREEN).
        """
        target_pairs = [("BLUE", "RED"), ("BLUE", "ORANGE"), ("ORANGE", "GREEN"), ("RED", "GREEN")]
        for color1, color2 in target_pairs:
            if not self.is_middle_edge_in_correct_position(color1, color2):
                return False
        return True

    def find_edge_with_colors(self, color1, color2):
        """Finds an edge piece that contains the given two colors."""
        # Define all 12 edge pieces with their positions on adjacent faces
        edges = [
            # Format: (face1, row1, col1, face2, row2, col2)
            ('U', 2, 1, 'F', 0, 1),  # U-F edge
            ('U', 1, 2, 'R', 0, 1),  # U-R edge  
            ('U', 0, 1, 'B', 0, 1),  # U-B edge
            ('U', 1, 0, 'L', 0, 1),  # U-L edge
            ('F', 1, 2, 'R', 1, 0),  # F-R edge
            ('F', 2, 1, 'D', 0, 1),  # F-D edge
            ('F', 1, 0, 'L', 1, 2),  # F-L edge
            ('R', 1, 2, 'B', 1, 0),  # R-B edge
            ('R', 2, 1, 'D', 1, 2),  # R-D edge
            ('B', 1, 2, 'L', 1, 0),  # B-L edge
            ('B', 2, 1, 'D', 2, 1),  # B-D edge
            ('L', 2, 1, 'D', 1, 0),  # L-D edge
        ]
        
        # Search through all edges
        for edge in edges:
            f1, r1, c1, f2, r2, c2 = edge
            c_on_f1 = self.faces[f1][r1][c1]
            c_on_f2 = self.faces[f2][r2][c2]
            if c_on_f1 == color1 and c_on_f2 == color2:
                return {
                    'face1': f1, 'position1': (r1, c1), 'color1': color1,
                    'face2': f2, 'position2': (r2, c2), 'color2': color2,
                    'edge_info': (f1, r1, c1, f2, r2, c2)
                }
            elif c_on_f1 == color2 and c_on_f2 == color1:
                # Swap so color1 is always first
                return {
                    'face1': f2, 'position1': (r2, c2), 'color1': color1,
                    'face2': f1, 'position2': (r1, c1), 'color2': color2,
                    'edge_info': (f2, r2, c2, f1, r1, c1)
                }        
        # If no edge found with those colors
        return None

    def get_edge_from_position(self, face, position):
        """Given a face and position, find the edge and return its information."""
        # Define all 12 edge pieces with their positions on adjacent faces
        edges = [
            # Format: (face1, row1, col1, face2, row2, col2)
            ('U', 2, 1, 'F', 0, 1),  # U-F edge
            ('U', 1, 2, 'R', 0, 1),  # U-R edge  
            ('U', 0, 1, 'B', 0, 1),  # U-B edge
            ('U', 1, 0, 'L', 0, 1),  # U-L edge
            ('F', 1, 2, 'R', 1, 0),  # F-R edge
            ('F', 2, 1, 'D', 0, 1),  # F-D edge
            ('F', 1, 0, 'L', 1, 2),  # F-L edge
            ('R', 1, 2, 'B', 1, 0),  # R-B edge
            ('R', 2, 1, 'D', 1, 2),  # R-D edge
            ('B', 1, 2, 'L', 1, 0),  # B-L edge
            ('B', 2, 1, 'D', 2, 1),  # B-D edge
            ('L', 2, 1, 'D', 1, 0),  # L-D edge
        ]
        
        row, col = position
        
        # Find the edge that contains this face and position
        for edge in edges:
            f1, r1, c1, f2, r2, c2 = edge
            if f1 == face and r1 == row and c1 == col:
                # Found it! Get colors from both sides
                color1 = self.faces[f1][r1][c1]
                color2 = self.faces[f2][r2][c2]
                
                # Ensure YELLOW is always first if present
                if color2 == "YELLOW" and color1 != "YELLOW":
                    color1, color2 = color2, color1
                
                # Use find_edge_with_colors to get full info
                return self.find_edge_with_colors(color1, color2)
            elif f2 == face and r2 == row and c2 == col:
                # Found it on the second side! Get colors from both sides
                color1 = self.faces[f1][r1][c1]
                color2 = self.faces[f2][r2][c2]
                
                # Ensure YELLOW is always first if present
                if color1 == "YELLOW" and color2 != "YELLOW":
                    # Keep as is - color1 is already YELLOW
                    pass
                elif color2 == "YELLOW" and color1 != "YELLOW":
                    color1, color2 = color2, color1
                
                # Use find_edge_with_colors to get full info
                return self.find_edge_with_colors(color1, color2)
        
        # Position not found in any edge
        return None
    







    
    def find_corner_with_colors(self, color1, color2, color3):
        # Always put WHITE last if present
        colors = [color1, color2, color3]
        if "WHITE" in colors and colors[2] != "WHITE":
            # Move WHITE to the end
            colors.remove("WHITE")
            colors.append("WHITE")
        color1, color2, color3 = colors

        corners = [
            ('U', 0, 0, 'L', 0, 0, 'B', 0, 2),
            ('U', 0, 2, 'B', 0, 0, 'R', 0, 2),
            ('U', 2, 0, 'F', 0, 0, 'L', 0, 2),
            ('U', 2, 2, 'R', 0, 0, 'F', 0, 2),
            ('D', 0, 0, 'L', 2, 2, 'F', 2, 0),
            ('D', 0, 2, 'F', 2, 2, 'R', 2, 0),
            ('D', 2, 0, 'B', 2, 2, 'L', 2, 0),
            ('D', 2, 2, 'R', 2, 2, 'B', 2, 0),
        ]
        for corner in corners:
            f1, r1, c1, f2, r2, c2, f3, r3, c3 = corner
            facelets = [
                (self.faces[f1][r1][c1], f1, (r1, c1)),
                (self.faces[f2][r2][c2], f2, (r2, c2)),
                (self.faces[f3][r3][c3], f3, (r3, c3)),
            ]
            facelet_colors = [fc[0] for fc in facelets]
            if set(facelet_colors) == set([color1, color2, color3]):
                # Map each color to its face and position
                mapping = {fc[0]: (fc[1], fc[2]) for fc in facelets}
                return {
                    'face1': mapping[color1][0], 'position1': mapping[color1][1], 'color1': color1,
                    'face2': mapping[color2][0], 'position2': mapping[color2][1], 'color2': color2,
                    'face3': mapping[color3][0], 'position3': mapping[color3][1], 'color3': color3,
                    'corner_info': (mapping[color1][0], mapping[color1][1],
                                    mapping[color2][0], mapping[color2][1],
                                    mapping[color3][0], mapping[color3][1])
                }
        return None

    def get_corner_from_position(self, face, position):
        """Given a face and position, find the corner and return its information.
        If YELLOW is present, it will always be returned as color3/face3/position3."""
        
        # All 8 corners with their 3 face positions
        corners = [
            ('U', 0, 0, 'L', 0, 0, 'B', 0, 2),
            ('U', 0, 2, 'B', 0, 0, 'R', 0, 2),
            ('U', 2, 0, 'F', 0, 0, 'L', 0, 2),
            ('U', 2, 2, 'R', 0, 0, 'F', 0, 2),
            ('D', 0, 0, 'L', 2, 2, 'F', 2, 0),
            ('D', 0, 2, 'F', 2, 2, 'R', 2, 0),
            ('D', 2, 0, 'B', 2, 2, 'L', 2, 0),
            ('D', 2, 2, 'R', 2, 2, 'B', 2, 0),
        ]
        
        row, col = position
        
        for corner in corners:
            f1, r1, c1, f2, r2, c2, f3, r3, c3 = corner
            
            # Check if the input face/position matches any of the 3 positions in this corner
            if f1 == face and r1 == row and c1 == col:
                # Get all 3 colors
                color1 = self.faces[f1][r1][c1]  # color from input position
                color2 = self.faces[f2][r2][c2]  # color from second position
                color3 = self.faces[f3][r3][c3]  # color from third position
                
            elif f2 == face and r2 == row and c2 == col:
                # Get all 3 colors
                color1 = self.faces[f2][r2][c2]  # color from input position
                color2 = self.faces[f1][r1][c1]  # color from first position
                color3 = self.faces[f3][r3][c3]  # color from third position
                
            elif f3 == face and r3 == row and c3 == col:
                # Get all 3 colors
                color1 = self.faces[f3][r3][c3]  # color from input position
                color2 = self.faces[f1][r1][c1]  # color from first position
                color3 = self.faces[f2][r2][c2]  # color from second position
                
            else:
                continue  # This corner doesn't contain the input position
            
            # Arrange colors so YELLOW is always last (color3) if present
            colors = [color1, color2, color3]
            if "YELLOW" in colors:
                colors.remove("YELLOW")
                colors.append("YELLOW")  # YELLOW becomes last
            
            return self.find_corner_with_colors(colors[0], colors[1], colors[2])
        
        return None




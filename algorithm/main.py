print("="*60)
print("         STARTING RUBIK'S CUBE SOLVER")
print("="*60)
import algorithm
import solve_white_cross
import solve_white_corners
import solve_middle_layer
import solve_yellow_face
import solve_last
import controls

import contextlib
import io
import json
import urllib.request
import atexit
from pathlib import Path



# Resolve cube file path robustly (prefer algorithm/cube_colors.txt)
script_dir = Path(__file__).resolve().parent
default_cube_file = script_dir / 'cube_colors.txt'
alt_cube_file = script_dir.parent / 'visualizer' / 'cube_colors.txt'
cube_file = default_cube_file if default_cube_file.exists() else alt_cube_file
print(f"[main.py] CWD: {Path.cwd()}")
print(f"[main.py] Using cube file: {cube_file}")

# Create the cube instance
cube = algorithm.RubiksCube(str(cube_file))

# Clear previous backend moves at start (best-effort)
try:
    req_clear = urllib.request.Request(
        "http://localhost:8001/moves/clear",
        data=b"{}",
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req_clear, timeout=5)
except Exception:
    pass

def _post_moves():
    try:
        payload = json.dumps({"moves_made": controls.anim_move_convert(), "moves": controls.anim_move_convert()}).encode("utf-8")
        req = urllib.request.Request(
            "http://localhost:8001/moves/set",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("[algorithm/main.py] /moves/set status:", resp.status)
    except Exception as e:
        print("[algorithm/main.py] Failed to send moves:", e)

# Always try to send whatever we have at process exit
atexit.register(_post_moves)

# Show initial state

print("\nInitial cube state:")
cube.visualize()
#SCRAMBLE
cube.visualize()

# Solve white cross
print("\n🔄 Solving white cross...")
solve_white_cross.solve_all_edges(cube)

# Check if white cross is solved and show final state
print("\n✅ White cross solved:", cube._is_white_cross_solved())
if not cube._is_white_cross_solved():
    print("white cross not solved")
    raise ValueError("White cross not solved")
print("\nCube state after white cross:")
cube.visualize()

print("\n" + "="*60)
print("         WHITE CROSS COMPLETE!")
print(controls.print_moves())
print("="*60)

# Test white corners (one at a time)
print("="*60)
print("="*60)
print("="*60)
print("="*60)
print("="*60)

print("Before corner")
#cube.visualize()
print("After corner")
#cube.visualize()


print("\n" + "="*60)
print("         CORNER TESTING COMPLETE!")
#controls.print_moves()
print("="*60) 
#controls.print_moves()
#cube.visualize()
# Solve white corners
print("\n🔄 Solving white corners...")
solve_white_corners.solve_all_corners(cube)

# Check if white corners are solved and show final state
print("\nCube state after white corners:")
cube.visualize()

print("\n" + "="*60)
print("\n✅ White corners solved:", cube._is_white_corners_solved())
if not cube._is_white_corners_solved():
    print("white corners not solved")
    raise ValueError("White corners not solved")
controls.print_moves()
print("="*60)
print(len(controls.moves_made))
print("middle layer")
cube.visualize()
controls.print_moves()

solve_middle_layer.solve_all_middle_edges(cube)
print("yellow face")
if not cube.is_middle_edges_solved():
    print("Middle edges not solved")
    raise ValueError("Middle edges not solved")
solve_yellow_face.solve_all_yellow_face(cube)

if not cube.is_yellow_face_solved():
    #exit()
    # print("Yellow face not solved")
    raise ValueError("Yellow face not solved")
print("after yellow face")
cube.visualize()
controls.print_moves()

print(" ".join(controls.moves_made))
print(f"Total moves: {len(controls.moves_made)}")

print("\n" + "="*60)
print("         DEBUGGING MOVE SEQUENCE")
print("="*60)
print("Final cube state after algorithm:")
cube.visualize()

print("\nMove sequence for visualizer:")
print("Raw moves (unfiltered):", controls.moves)
print("Optimized moves (filtered):", controls.moves_made)
print("Raw moves formatted:", " ".join(controls.moves))
print("Optimized moves formatted:", " ".join(controls.moves_made))
print(f"Raw move count: {len(controls.moves)}")
print(f"Optimized move count: {len(controls.moves_made)}")

print("\nDifference analysis:")
if len(controls.moves) != len(controls.moves_made):
    print(f"⚠️  Move count differs! Raw: {len(controls.moves)}, Optimized: {len(controls.moves_made)}")
    print("Optimization removed", len(controls.moves) - len(controls.moves_made), "moves")
else:
    print("✅ Move counts match - no optimization occurred")

print("\nInitial vs Final comparison:")
print("If this doesn't match your visualizer, check:")
print("1. Move notation format (F' vs Fi vs F3)")
print("2. Starting cube orientation")
print("3. Color-to-face mapping")
print("="*60+"\n")
print("="*60)
cube.visualize()
solve_last.solve(cube)
print("after last")
cube.visualize()
print(f"Total moves: {len(controls.moves_made)}")
controls.print_moves()
_post_moves()
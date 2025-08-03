import algorithm
import solve_white_cross
import solve_white_corners
import controls
import contextlib
import io
# Create the cube instance
cube = algorithm.RubiksCube('cube_colors.txt')

print("="*60)
print("         STARTING RUBIK'S CUBE SOLVER")
print("="*60)

# Show initial state
print("\nInitial cube state:")
cube.visualize()
#SCRAMBLE
controls.D_prime(cube); controls.L(cube); controls.B_prime(cube); controls.R(cube); controls.U(cube); controls.F_prime(cube); controls.D(cube); controls.R_prime(cube); controls.B(cube); controls.L_prime(cube); controls.U_prime(cube); controls.F(cube); controls.R(cube); controls.D_prime(cube); controls.B_prime(cube); controls.U(cube); controls.L(cube); controls.F_prime(cube); controls.R_prime(cube); controls.D(cube)
print("\nScrambled cube:")
cube.visualize()

# Solve white cross
print("\n🔄 Solving white cross...")
solve_white_cross.solve_all_edges(cube)

# Check if white cross is solved and show final state
print("\n✅ White cross solved:", cube._is_white_cross_solved())
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
def silent_call(func, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)
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
controls.print_moves()
print("="*60)


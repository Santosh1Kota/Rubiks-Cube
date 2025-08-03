from algorithm import RubiksCube
import controls

# Create a cube instance
cube = RubiksCube('cube_colors.txt')
cube.visualize()
print("\n\n\n\n")

#START FROM U TOMORROW
color1 = "ORANGE"
color2 = "WHITE"
info = cube.find_edge_with_colors(color1, color2)
print(info)
controls.B_prime(cube)
info = cube.find_edge_with_colors(color1, color2)
print(info)

controls.B_prime(cube)
info = cube.find_edge_with_colors(color1, color2)
print(info)
cube.visualize()

# print("ORIGINAL CUBE:")
# cube.visualize()

# print("\n" + "="*50)
# print("TESTING SINGLE MOVES:")
# print("="*50)

# # Test R move
# print("Testing  d move:")
# controls.R(cube)
# cube.visualize()

# # Test R' move to undo
# print("Testing R' move (should undo R):")
# controls.R_prime(cube)
# cube.visualize()

# print("Class works correctly - no automatic solving!")



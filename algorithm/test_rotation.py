from controls import rotate_face_clockwise, rotate_face_counterclockwise

# Test with a simple 3x3 grid
test_face = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Original face:")
for row in test_face:
    print(row)

print("\nClockwise rotation:")
clockwise_result = rotate_face_clockwise(test_face)
for row in clockwise_result:
    print(row)

print("\nCounterclockwise rotation:")
counterclockwise_result = rotate_face_counterclockwise(test_face)
for row in counterclockwise_result:
    print(row)

# Test if doing clockwise then counterclockwise gets back to original
print("\nClockwise then counterclockwise (should be original):")
back_to_original = rotate_face_counterclockwise(clockwise_result)
for row in back_to_original:
    print(row)

# Check if they're inverses
print(f"\nAre they inverses? {test_face == back_to_original}")

# Test the other way: counterclockwise then clockwise
print("\nCounterclockwise then clockwise (should be original):")
back_to_original2 = rotate_face_clockwise(counterclockwise_result)
for row in back_to_original2:
    print(row)

print(f"Are they inverses (other direction)? {test_face == back_to_original2}") 
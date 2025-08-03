from inference import get_model
import supervision as sv
import cv2
import numpy as np
from sklearn.cluster import KMeans
import itertools
import datetime
import os
import shutil
# Face instructions in order
face_order = [
    ("F", "Hold cube with WHITE center facing camera", "GREEN center should face UP"),
    ("R", "Rotate cube 90 degrees left", "RED center should face camera, Green center should face UP"),
    ("B", "Rotate cube 90 degrees left", "YELLOW center should face camera, Green center should face UP"),
    ("L", "Rotate cube 90 degrees left", "ORANGE center should face camera, Green center should face UP"),
    ("U", "Rotate so GREEN center faces camera", "RED center should face UP"),
    ("D", "Rotate 180 degrees cube so BLUE center faces camera", "RED center should face UP")
]

face_idx = 0

def get_center(box):
    # box: [x_min, y_min, x_max, y_max]
    x_center = (box[0] + box[2]) / 2
    y_center = (box[1] + box[3]) / 2
    return (x_center, y_center)

def filter_best_9_tiles(detections):
    if len(detections) <= 9:
        return detections  # Already fine

    best_score = float('inf')
    best_group_indices = None

    all_indices = range(len(detections))
    for group_indices in itertools.combinations(all_indices, 9):
        centers = np.array([get_center(detections.xyxy[i]) for i in group_indices])
        xs, ys = centers[:, 0], centers[:, 1]

        try:
            row_labels = cluster_axis(ys)
            col_labels = cluster_axis(xs)
        except:
            continue

        if len(set(row_labels)) != 3 or len(set(col_labels)) != 3:
            continue

        row_vals = sorted(set(ys))
        col_vals = sorted(set(xs))
        if len(row_vals) < 3 or len(col_vals) < 3:
            continue

        row_diffs = np.diff(row_vals)
        col_diffs = np.diff(col_vals)
        score = np.var(row_diffs) + np.var(col_diffs)

        if score < best_score:
            best_score = score
            best_group_indices = group_indices

    if best_group_indices:
        return detections[list(best_group_indices)]
    else:
        print("⚠️ Could not find a grid-like set of 9 tiles.")
        return detections  # fallback to all if clustering fails
# Helper to cluster 3 rows or 3 cols using k-means

def cluster_axis(vals):
    vals = np.array(vals).reshape(-1, 1)
    kmeans = KMeans(n_clusters=3, n_init="auto").fit(vals)
    return kmeans.labels_
def get_color(predictions):
    predictions = predictions["predictions"]
    print(predictions)
    if len(predictions) != 9:
        raise ValueError("Expected exactly 9 predictions to form a 3x3 grid.")

    predictions.sort(key=lambda t: t["y"])
    rows = [predictions[i:i+3] for i in range(0, 9, 3)]
    for row in rows:
        row.sort(key=lambda t: t["x"])

    color_grid = []
    for row in rows:
        color_row = []
        for tile in row:
            color_name = tile["class"]
            if color_name not in class_id_to_name.values():
                print(f"⚠️ Warning: Unknown color name: '{color_name}'")
            color_row.append(color_name)
        color_grid.append(color_row)

    return np.array(color_grid)

def update_cube_face(cube, face_label, predictions):
    try:
        color_grid = get_color(predictions)
        # Apply face-specific rotation fix
        if face_label == "U":
            color_grid = np.rot90(color_grid, k=-1)  # 90° clockwise
            color_grid = np.rot90(color_grid, k=-1)  # 90° clockwise
        elif face_label == "R":
            color_grid = np.rot90(color_grid, k=1)   # 90° counterclockwise
        elif face_label == "L":
            color_grid = np.rot90(color_grid, k=-1)  # 90° clockwise
        elif face_label == "B":
            color_grid = np.rot90(color_grid, k=2)   # 180°
        elif face_label == "D":
            color_grid = np.rot90(color_grid, k=1)   # 90° counterclockwise

        cube[face_label] = color_grid.tolist()
        print(f"✅ Updated face '{face_label}' successfully.")
    except Exception as e:
        print(f"❌ Failed to update face '{face_label}': {e}")

# Map from class_id to class name - adjust according to your model's class names
class_id_to_name = {
    0: "BLUE",
    2: "GREEN",
    3: "ORANGE",
    4: "RED",
    5: "WHITE",
    6: "YELLOW"
}

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("❌ Cannot access webcam.")

print("📦 Rubik's Cube Scanner Started")
print("🧠 Loading detection model...")

model = get_model(model_id="rubik-s-cube-sticker-detection-rxdj9/4", api_key="6F3leq34c4JjHUoljYcJ")
print("✅ Model loaded successfully!")

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

min_confidence = 0.7
image_count = 1
paused_on_result = False
retake = False
current_frame = None

cube = {f: [[""]*3 for _ in range(3)] for f in ['U', 'F', 'R', 'L', 'B', 'D']}

print("\n🎮 Controls:")
print("  [SPACE]  - Capture current cube face")
print("  [Y]      - Confirm detection is correct")
print("  [N]      - Reject and retake image")
print("  [→]      - Skip/continue to next face")
print("  [ESC]    - Quit anytime\n")

while face_idx < len(face_order):
    face_label, text1, text2 = face_order[face_idx]

    if not paused_on_result:
        ret, frame = cap.read()
        if not ret:
            print("❌ Webcam read failed.")
            break
        current_frame = frame.copy()
        frame_with_text = frame.copy()

        cv2.putText(frame_with_text, f"Face: {face_label}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(frame_with_text, text1, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        cv2.putText(frame_with_text, text2, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Rubik's Cube Scanner", frame_with_text)

    key = cv2.waitKeyEx(1)
    if key == 27:  # ESC
        print("👋 Exiting.")
        break

    elif key == 32 and not paused_on_result:  # SPACE
        print(f"\n📸 Capturing Face: {face_label}")
        results = model.infer(current_frame)[0]

        detections = sv.Detections.from_inference(results)
        detections = detections.with_nms(threshold=0.5)
        detections = detections[detections.confidence > min_confidence]
        if (len(detections)>9):
            detections = filter_best_9_tiles(detections)
        print("Detected class IDs:", detections.class_id.tolist())

        print(f"🔍 {len(detections)} tile(s) detected.")

        annotated = box_annotator.annotate(scene=current_frame.copy(), detections=detections)
        annotated = label_annotator.annotate(scene=annotated, detections=detections)
        paused_on_result = True
        image_count += 1

        while True:
            msg_frame = annotated.copy()
            cv2.putText(msg_frame, "Is this detection accurate? (Y/N)", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.imshow("Rubik's Cube Scanner", msg_frame)
            key = cv2.waitKeyEx(0)

            if key == 121:  # 'y'
                if len(detections) != 9:
                    print("❌ Not 9 tiles! Please retake.")
                    cv2.putText(msg_frame, "Exactly 9 tiles must be detected!", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow("Rubik's Cube Scanner", msg_frame)
                    retake = True
                else:
                    print("✅ Detection confirmed.")

                    # Build filtered predictions for update_cube_face
                    filtered_predictions = []
                    for i in range(len(detections)):
                        x = detections.xyxy[i][0].item()
                        y = detections.xyxy[i][1].item()
                        class_id = detections.class_id[i]
                        class_name = class_id_to_name.get(class_id, f"class_{class_id}")
                        filtered_predictions.append({
                            "x": x,
                            "y": y,
                            "class": class_name
                        })

                    update_cube_face(cube, face_label, {"predictions": filtered_predictions})

                    print(f"➡️ Proceeding to next face...\n")
                    retake = False
                    face_idx += 1
                    paused_on_result = False
                break

            elif key == 110:  # 'n'
                print("🔁 Retaking face image...")
                msg_frame = annotated.copy()
                cv2.putText(msg_frame, "❌ Retake the image!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.imshow("Rubik's Cube Scanner", msg_frame)
                retake = True
                break

            elif key == 27:
                print("👋 Exiting.")
                cap.release()
                cv2.destroyAllWindows()
                exit()

    elif (paused_on_result and key == 63235) or retake:  # RIGHT ARROW
        print("▶️ Skipping or reattempting...")
        paused_on_result = False
        retake = False

# Clean up
cap.release()
cv2.destroyAllWindows()
#UP WORKS DOWN COMMENTED IS THE WORKING OLD ONE
# Final cube output


# Add this function to your existing Python script

def apply_transformations(cube):
    def flip_rows(grid):
        return [row[::-1] for row in grid]

    def rotate90_cw(grid):
        return [list(reversed(col)) for col in zip(*grid)]

    def rotate180(grid):
        return [list(reversed(row)) for row in reversed(grid)]

    transformed = {}
    for face, grid in cube.items():
        grid = [row.copy() for row in grid]  # deep copy to avoid mutating original

        # Common vertical mirror
        grid = grid[::-1]

        if face == "F":
            grid = flip_rows(grid)  # 180
        elif face == "L":
            grid = rotate90_cw(grid)  # 90 CW
        elif face == "B":
            grid = rotate180(grid)
            grid = flip_rows(grid)
        elif face == "D":
            grid = rotate180(grid)
        elif face == "R":
            grid = rotate180(grid)
            grid = rotate90_cw(grid)
        elif face == "U":
            grid = rotate90_cw(grid)

        transformed[face] = grid
    return transformed


# Replace your export section with this:

# Final cube output
print("\n🎉 Cube Scanning Complete!")

transformed_cube = apply_transformations(cube)
for face in transformed_cube:
    print(f"{face}:\n{np.array(transformed_cube[face])}\n")

# Export cube to TXT format
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"cube_colors.txt"

# Define the two save locations
current_dir = os.getcwd()  # Current directory (rubix)
processing_dir = "/Users/santoshkota/Documents/Processing"  # TODO: User will provide exact path later

# Create the file content
file_content = ""
for face in ['U', 'F', 'R', 'L', 'B', 'D']:
    colors = [color for row in transformed_cube[face] for color in row]
    line = f"{face} {' '.join(colors)}\n"
    file_content += line

# Save to first location (current directory)
try:
    current_path = os.path.join(current_dir, filename)
    with open(current_path, 'w') as f:
        f.write(file_content)
    print(f"✅ Cube data exported to: {current_path}")
except Exception as e:
    print(f"❌ Failed to export TXT to current directory: {e}")

# Save to second location (processing directory)
try:
    # Create processing directory if it doesn't exist
    #os.makedirs(processing_dir, exist_ok=True)
    processing_dir = "/Users/santoshkota/Documents/Processing/rubiks_cube"
    
    processing_path = os.path.join(processing_dir, filename)
    with open(processing_path, 'w') as f:
        f.write(file_content)
    print(f"✅ Cube data also exported to: {processing_path}")
except Exception as e:
    print(f"❌ Failed to export TXT to processing directory: {e}")

print("📁 Format: Each line contains face letter + 9 colors")

# print("🎉 Cube Scanning Complete!")

# for face in cube:
#     print(f"{face}:\n{np.array(cube[face])}\n")

# # Export cube to TXT format
# timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"rubiks_cube_{timestamp}.txt"

# try:
#     with open(filename, 'w') as f:
#         # Export each face in the specified format
#         for face in ['U', 'F', 'R', 'L', 'B', 'D']:
#             # Flatten the 3x3 grid into a single line of 9 colors
#             colors = []
#             for row in cube[face]:
#                 for color in row:
#                     colors.append(color if color else "UNKNOWN")
            
#             # Write face letter followed by 9 colors
#             line = f"{face} {' '.join(colors)}\n"
#             f.write(line)
    
#     print(f"✅ Cube data exported to: {filename}")
#     print(f"📁 Format: Each line contains face letter + 9 colors")
# except Exception as e:
#     print(f"❌ Failed to export TXT: {e}")


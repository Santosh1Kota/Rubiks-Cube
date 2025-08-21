
from inference import get_model
import supervision as sv
import cv2
import numpy as np
from sklearn.cluster import KMeans
import itertools
import datetime
import os
from typing import Dict, List, Any, Optional
from PIL import Image
from io import BytesIO
import base64

# Map from class_id to class name - adjust according to your model's class names
class_id_to_name = {
    0: "BLUE",
    2: "GREEN", 
    3: "ORANGE",
    4: "RED",
    5: "WHITE",
    6: "YELLOW"
}

# Global model instance
_model = None

def init_model(api_key: str = "6F3leq34c4JjHUoljYcJ"):
    """Initialize the Roboflow model once."""
    global _model
    if _model is None:
        _model = get_model(model_id="rubik-s-cube-sticker-detection-rxdj9/4", api_key=api_key)
    return _model

def get_center(box):
    """Get center point of bounding box."""
    # box: [x_min, y_min, x_max, y_max] 
    x_center = (box[0] + box[2]) / 2
    y_center = (box[1] + box[3]) / 2
    return (x_center, y_center)

def cluster_axis(vals):
    """Helper to cluster 3 rows or 3 cols using k-means."""
    vals = np.array(vals).reshape(-1, 1)
    kmeans = KMeans(n_clusters=3, n_init="auto").fit(vals)
    return kmeans.labels_

def filter_best_9_tiles(detections):
    """Filter detections to best 9 tiles that form a grid."""
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

def get_color(predictions):
    """Convert predictions to 3x3 color grid, exactly like original model.py."""
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
    """Update cube face with predictions, applying face-specific rotations like original."""
    try:
        color_grid = get_color(predictions)
        # Apply face-specific rotation fix - EXACT same logic as original
        if face_label == "U":
            pass  # No rotation for U
        elif face_label == "R":
            pass  # No rotation for R
        elif face_label == "L":
            pass  # No rotation for L
        elif face_label == "B":
            pass  # No rotation for B
        elif face_label == "D":
            pass  # No rotation for D

        cube[face_label] = color_grid.tolist()
        print(f"✅ Updated face '{face_label}' successfully.")
        return color_grid.tolist()
    except Exception as e:
        print(f"❌ Failed to update face '{face_label}': {e}")
        return None

def apply_transformations(cube):
    """Apply final transformations to cube - EXACT same logic as original."""
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

def process_single_face(image_bytes: bytes, face_label: str, min_confidence: float = 0.7) -> Dict[str, Any]:
    """
    Process a single face image using the exact same logic as model.py.
    
    Args:
        image_bytes: Raw image bytes
        face_label: Face label (U, R, F, D, L, B)
        min_confidence: Minimum confidence threshold
        
    Returns:
        Dict containing predictions, color_grid, annotated_image, and success status
    """
    try:
        # Initialize model
        model = init_model()
        
        # Load image from bytes (convert to OpenCV format like original)
        img_array = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if frame is None:
            return {"error": "Could not decode image", "success": False}
        
        print(f"\n📸 Processing Face: {face_label}")
        
        # Run inference - EXACT same as original model.py line 179
        results = model.infer(frame)[0]
        
        # Process detections - EXACT same as original model.py lines 181-185
        detections = sv.Detections.from_inference(results)
        detections = detections.with_nms(threshold=0.5)
        detections = detections[detections.confidence > min_confidence]
        if len(detections) > 9:
            detections = filter_best_9_tiles(detections)
        
        print("Detected class IDs:", detections.class_id.tolist())
        print(f"🔍 {len(detections)} tile(s) detected.")
        
        # Create annotated image - EXACT same as original model.py lines 190-191
        box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()
        annotated = box_annotator.annotate(scene=frame.copy(), detections=detections)
        annotated = label_annotator.annotate(scene=annotated, detections=detections)
        
        # Check if we have exactly 9 detections
        if len(detections) != 9:
            return {
                "error": f"Expected 9 tiles, got {len(detections)}",
                "success": False,
                "detections_count": len(detections),
                "annotated_image": annotated
            }
        
        # Build filtered predictions - EXACT same as original model.py lines 211-221
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
        
        # Create cube structure and update face
        cube = {f: [[""]*3 for _ in range(3)] for f in ['U', 'F', 'R', 'L', 'B', 'D']}
        color_grid = update_cube_face(cube, face_label, {"predictions": filtered_predictions})
        
        return {
            "success": True,
            "face": face_label,
            "predictions": filtered_predictions,
            "color_grid": color_grid,
            "annotated_image": annotated,
            "detections_count": len(detections)
        }
        
    except Exception as e:
        print(f"❌ Error processing face {face_label}: {e}")
        return {"error": str(e), "success": False}

def annotated_image_to_bytes(annotated_image, format='JPEG', quality=90) -> bytes:
    """Convert OpenCV image to bytes."""
    # Convert BGR to RGB for PIL
    rgb_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    
    buffer = BytesIO()
    pil_image.save(buffer, format=format, quality=quality)
    return buffer.getvalue()

def annotated_image_to_base64(annotated_image, format='JPEG', quality=90) -> str:
    """Convert OpenCV image to base64 data URL."""
    image_bytes = annotated_image_to_bytes(annotated_image, format, quality)
    b64_string = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/{format.lower()};base64,{b64_string}"

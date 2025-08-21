"""
Cube Processor - Stateful face processing extracted from model.py

This module provides a stateful function to process cube faces one by one,
building up a complete cube representation that can be used for visualization.
"""

import numpy as np
from sklearn.cluster import KMeans
import itertools
from typing import Dict, List, Any, Optional

# Global cube state - will be updated as faces are processed
cube_state = {f: [[""]*3 for _ in range(3)] for f in ['U', 'F', 'R', 'L', 'B', 'D']}

# Map from class_id to class name - should match model.py
class_id_to_name = {
    0: "BLUE",
    2: "GREEN", 
    3: "ORANGE",
    4: "RED",
    5: "WHITE",
    6: "YELLOW"
}

def reset_cube():
    """Reset the global cube state to empty."""
    global cube_state
    cube_state = {f: [[""]*3 for _ in range(3)] for f in ['U', 'F', 'R', 'L', 'B', 'D']}
    print("🔄 Cube state reset")

def get_cube_state():
    """Get the current complete cube state."""
    return cube_state.copy()

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
    """Filter detections to best 9 tiles that form a grid (from model.py)."""
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
    """Convert predictions to 3x3 color grid (from model.py)."""
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
    """Update cube face with predictions, applying rotations (from model.py)."""
    try:
        color_grid = get_color(predictions)
        # Apply face-specific rotation fix (same as model.py)
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
        return True
    except Exception as e:
        print(f"❌ Failed to update face '{face_label}': {e}")
        return False

def process_face(predictions, face_label: str, detections=None, min_confidence=0.7) -> Dict:
    print(f"Processing facer: {face_label}")
    """
    Process a single cube face with Roboflow predictions.
    Includes all validation logic from model.py.
    
    Args:
        predictions: Complete predictions object from Roboflow (same format as model.py expects)
        face_label: Face identifier ('F', 'R', 'B', 'L', 'U', 'D')
        detections: Optional detections object for tile count validation
    
    Returns:
        Dict containing:
        - success: bool
        - cube_state: complete updated cube state
        - face_data: 3x3 array for this specific face
        - message: status message
        - needs_retake: bool (if validation failed)
        - detections_count: number of tiles detected
    """
    global cube_state
    
    try:
        print(f"📸 Processing Face: {face_label}")
        
        # Validate face label
        if face_label not in ['F', 'R', 'B', 'L', 'U', 'D']:
            return {
                "success": False,
                "error": f"Invalid face label: {face_label}",
                "cube_state": cube_state,
                "needs_retake": False,
                "detections_count": 0
            }
        
        # Count detections - CRITICAL validation from model.py
        if isinstance(predictions, dict) and "predictions" in predictions:
            raw_predictions = predictions["predictions"]
            detections_count = len(raw_predictions)
        else:
            raw_predictions = predictions if predictions else []
            detections_count = len(raw_predictions)
        
        print(f"🔍 {detections_count} tile(s) detected.")
        
        # Apply confidence filtering (from model.py line 183)
        filtered_predictions = []
        if raw_predictions:
            for pred in raw_predictions:
                confidence = pred.get("confidence", 1.0)  # Default to 1.0 if missing
                if confidence >= min_confidence:
                    filtered_predictions.append(pred)
                else:
                    print(f"⚠️ Filtered out prediction with confidence {confidence:.2f} < {min_confidence}")
        
        final_count = len(filtered_predictions)
        print(f"🔍 {final_count} tile(s) after confidence filtering (≥{min_confidence}).")
        
        # CRITICAL: Exactly 9 tiles validation (from model.py line 202-207)
        if final_count != 9:
            error_msg = f"❌ Expected exactly 9 tiles, got {final_count}. Please retake."
            print(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "cube_state": cube_state,
                "needs_retake": True,  # This signals frontend to allow retake
                "detections_count": final_count
            }
        
        # Check if face already processed
        current_face_data = cube_state.get(face_label, [[""]*3 for _ in range(3)])
        is_already_filled = any(any(cell != "" for cell in row) for row in current_face_data)
        
        if is_already_filled:
            print(f"⚠️ Face {face_label} already processed. Overwriting...")
        
        # Process the face using filtered predictions (this modifies cube_state globally)
        filtered_predictions_dict = {"predictions": filtered_predictions}
        success = update_cube_face(cube_state, face_label, filtered_predictions_dict)
        print("CUBIE STATE",filtered_predictions)
        if success:
            return {
                "success": True,
                "cube_state": cube_state,
                "face_data": cube_state[face_label],
                "message": f"✅ Face {face_label} processed successfully",
                "needs_retake": False,
                "detections_count": final_count
            }
        else:
            return {
                "success": False,
                "error": f"❌ Failed to process face {face_label} - color grid creation failed",
                "cube_state": cube_state,
                "needs_retake": True,
                "detections_count": final_count
            }
    
    except ValueError as e:
        # Handle specific ValueError (like "Expected exactly 9 predictions")
        error_msg = f"❌ Validation error for face {face_label}: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "cube_state": cube_state,
            "needs_retake": True,
            "detections_count": final_count if 'final_count' in locals() else 0
        }
    except Exception as e:
        error_msg = f"❌ Unexpected error processing face {face_label}: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "cube_state": cube_state,
            "needs_retake": True,
            "detections_count": final_count if 'final_count' in locals() else 0
        }
    

def apply_transformations(cube):
    """
    Apply final transformations to cube for export (from model.py).
    This is used for creating the final output format.
    """
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

def get_completion_status():
    """Check which faces have been completed."""
    completed_faces = []
    for face, grid in cube_state.items():
        # Check if face has any non-empty cells
        has_data = any(any(cell != "" for cell in row) for row in grid)
        if has_data:
            completed_faces.append(face)
    
    return {
        "completed_faces": completed_faces,
        "total_faces": len(completed_faces),
        "is_complete": len(completed_faces) == 6,
        "remaining_faces": [f for f in ['F', 'R', 'B', 'L', 'U', 'D'] if f not in completed_faces]
    }

def export_cube_data():
    """
    Export cube state with explicit per-face rotations for the solver.
    This does NOT affect AnimCube facelets.
    """
    if get_completion_status()["is_complete"]:
        # Helper transforms
        def rotate90_cw(grid: list[list[str]]) -> list[list[str]]:
            n = len(grid)
            res = [["" for _ in range(n)] for _ in range(n)]
            for r in range(n):
                for c in range(n):
                    res[c][n - 1 - r] = grid[r][c]
            return res

        def rotate180(grid: list[list[str]]) -> list[list[str]]:
            return rotate90_cw(rotate90_cw(grid))

        def rotate270_cw(grid: list[list[str]]) -> list[list[str]]:
            return rotate90_cw(rotate180(grid))

        def flip_cols(grid: list[list[str]]) -> list[list[str]]:
            # Mirror horizontally (swap columns)
            return [row[::-1] for row in grid]

        # Deep copy current state
        export_cube = {f: [row.copy() for row in cube_state[f]] for f in ['U','F','R','L','B','D']}
        try:
            print("[EXPORT] pre U:", cube_state['U'])
            print("[EXPORT] pre L:", cube_state['L'])
            print("[EXPORT] pre R:", cube_state['R'])
            print("[EXPORT] pre D:", cube_state['D'])
        except Exception:
            pass

        # Apply requested transforms (clockwise where applicable):
        # U: 90° CW
        export_cube['U'] = rotate90_cw(export_cube['U'])
        # L: 90° CW
        export_cube['L'] = rotate90_cw(export_cube['L'])
        # R: 90° CCW → 270° CW
        export_cube['R'] = rotate270_cw(export_cube['R'])
        # D: reflected (mirror columns)
        export_cube['D'] = flip_cols(export_cube['D'])
        # F, B unchanged
        try:
            print("[EXPORT] post U:", export_cube['U'])
            print("[EXPORT] post L:", export_cube['L'])
            print("[EXPORT] post R:", export_cube['R'])
            print("[EXPORT] post D:", export_cube['D'])
        except Exception:
            pass

        # Create file content from export_cube (row-major) in algorithm's face order
        file_content = ""
        for face in ['U', 'F', 'R', 'L', 'B', 'D']:
            colors = [color for row in export_cube[face] for color in row]
            line = f"{face} {' '.join(colors)}\n"
            file_content += line
        
        return {
            "success": True,
            "cube_data": export_cube,
            "file_content": file_content
        }
    else:
        return {
            "success": False,
            "error": "Cube not complete - need all 6 faces"
        }

def export_cube_data_force():
    """
    Export whatever is currently captured, applying the same per-face
    rotations as export_cube_data(), without requiring completion.
    Missing stickers are left as empty strings.
    """
    # Helper transforms
    def rotate90_cw(grid: list[list[str]]) -> list[list[str]]:
        n = len(grid)
        res = [["" for _ in range(n)] for _ in range(n)]
        for r in range(n):
            for c in range(n):
                res[c][n - 1 - r] = grid[r][c]
        return res

    def rotate180(grid: list[list[str]]) -> list[list[str]]:
        return rotate90_cw(rotate90_cw(grid))

    def rotate270_cw(grid: list[list[str]]) -> list[list[str]]:
        return rotate90_cw(rotate180(grid))

    def flip_cols(grid: list[list[str]]) -> list[list[str]]:
        return [row[::-1] for row in grid]

    export_cube = {f: [row.copy() for row in cube_state[f]] for f in ['U','F','R','L','B','D']}
    # Match export_cube_data spec:
    # U: 90° CW
    export_cube['U'] = rotate90_cw(export_cube['U'])
    # L: 90° CW
    export_cube['L'] = rotate90_cw(export_cube['L'])
    # R: 90° CCW → 270° CW
    export_cube['R'] = rotate270_cw(export_cube['R'])
    # D: mirror horizontally
    export_cube['D'] = flip_cols(export_cube['D'])

    file_content = ""
    for face in ['U', 'F', 'R', 'L', 'B', 'D']:
        colors = [color for row in export_cube[face] for color in row]
        line = f"{face} {' '.join(colors)}\n"
        file_content += line

    return {
        "success": True,
        "cube_data": export_cube,
        "file_content": file_content
    }

if __name__ == "__main__":
    # Test/demo code
    print("Cube Processor Module")
    print("Global cube state:", cube_state)
    print("Completion status:", get_completion_status())

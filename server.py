from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import re
import base64
from pathlib import Path
import json
from typing import Dict, Any, List
from io import BytesIO
from fastapi import Response
from fastapi import Body
import subprocess
import sys

# Optional local inference via model_api (avoids running model.py main code)
try:
    from PIL import Image, ImageDraw
except Exception:
    Image = None
    ImageDraw = None

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

import requests

# Import your existing algorithm modules and controls
# Adjust imports if your package structure differs
try:
    import algorithm.controls as controls
    # Example staged solvers (uncomment and use when ready)
    # import algorithm.solve_white_cross as swc
    # import algorithm.solve_white_corners as swcr
    # import algorithm.solve_middle_layer as sml
    # import algorithm.solve_yellow_face as syf
    # import algorithm.solve_last as sl
except Exception:
    controls = None  # Fallback if not available yet

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Facelets helpers (no rotations, order matches cube net: U, D, F, B, L, R)
COLOR_TO_FACELET = {
    "WHITE": "w",
    "YELLOW": "y",
    "ORANGE": "o",
    "RED": "r",
    "GREEN": "g",
    "BLUE": "b",
}
FACE_ORDER = ["U", "D", "F", "B", "L", "R"]

def cube_state_to_facelets(state: dict | None) -> str:
    if not state:
        return ""
    facelet_list = []
    for i in range(2,-1,-1):
        for j in range(0,3):
            facelet_list.append(state.get('F')[i][j])
    for j in range(2,-1,-1):
        for i in range(2,-1,-1):
            facelet_list.append(state.get('B')[i][j])
    for j in range(0,3):
        for i in range(0,3):
            facelet_list.append(state.get('D')[i][j])
    for j in range(2,-1,-1):
        for i in range(2,-1,-1):
            facelet_list.append(state.get('U')[i][j])
    for j in range(2,-1,-1):
        for i in range(2,-1,-1):
            facelet_list.append(state.get('L')[i][j])
    for i in range(2,-1,-1):
        for j in range(0,3):
            facelet_list.append(state.get('R')[i][j])
    print("FACELET LIST: ",facelet_list)
    # Map colors -> single-letter facelets and return 54-char string built from facelet_list
    return "".join(COLOR_TO_FACELET.get(color, "g") for color in facelet_list)


def send_facelets(facelets: str) -> None:
    """
    Placeholder hook: implement your own delivery (e.g., POST to another service).
    Example (to fill in):
        import urllib.request, json
        req = urllib.request.Request("http://example.com/facelets", data=json.dumps({"facelets": facelets}).encode("utf-8"), headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    """
    pass


def reset_moves():
    if controls is not None:
        try:
            controls.moves.clear()
            controls.moves_made.clear()
        except Exception:
            pass


def solve_from_state_stub() -> List[str]:
    """Placeholder solve: return a short static sequence until classifier/solver is wired."""
    return ["F", "R", "U'", "R'", "F'"]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "roboflow_configured": bool(os.getenv("ROBOFLOW_API_KEY")),
        "workspace": os.getenv("ROBOFLOW_WORKSPACE") or None,
        "workflow_id": os.getenv("ROBOFLOW_WORKFLOW_ID") or None,
    }


@app.post("/solve")
async def solve(image: UploadFile = File(...)):
    # TODO: Replace with actual classification + solving
    # - Read bytes: await image.read()
    # - Detect cube state
    # - Build cube and run staged solver
    reset_moves()
    moves = solve_from_state_stub()
    return {"moves": moves}


@app.post("/detect")
async def detect(
    file: UploadFile = File(...),
    face: str | None = Form(None),
):
    """Run Roboflow Hosted Inference and return predictions and an annotated image preview.

    This implementation uses detect.roboflow.com for a concrete visualization image.
    It also saves the returned image to roboflow_downloads/roboflow_image.jpg.
    """
    api_key = os.getenv("ROBOFLOW_API_KEY")
    model_id = os.getenv("ROBOFLOW_MODEL_ID", "rubik-s-cube-sticker-detection-rxdj9/4")
    if not api_key:
        return {"error": "ROBOFLOW_API_KEY not set", "roboflow_configured": False}

    content = await file.read()
    filename = file.filename or "image.jpg"

    try:
        # 1) JSON predictions
        json_url = f"https://detect.roboflow.com/{model_id}?api_key={api_key}"
        json_resp = requests.post(json_url, files={"file": (filename, content, file.content_type or "image/jpeg")}, timeout=60)
        json_resp.raise_for_status()
        result = json_resp.json()

        # 2) Annotated image
        image_url = f"https://detect.roboflow.com/{model_id}?api_key={api_key}&format=image"
        img_resp = requests.post(image_url, files={"file": (filename, content, file.content_type or "image/jpeg")}, timeout=60)
        img_resp.raise_for_status()
        image_bytes = img_resp.content

        # Save locally
        out_dir = Path(os.getenv("ROBOFLOW_PREVIEW_DIR", "roboflow_downloads")).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "roboflow_image.jpg"
        with open(out_path, "wb") as f:
            f.write(image_bytes)

        preview_data_url = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
        return {
            "face": face,
            "result": result,
            "preview": preview_data_url,
            "preview_file": str(out_path),
            "model_id": model_id,
        }
    except requests.RequestException as e:
        return {"face": face, "error": str(e), "status": getattr(e.response, "status_code", None)}


def _build_color_grid_from_predictions(preds: List[Dict[str, Any]]) -> List[List[str]]:
    """Given predictions with x,y,class, build a 3x3 color grid ordered by y then x."""
    if len(preds) < 9:
        preds = sorted(preds, key=lambda p: (p.get("y", 0), p.get("x", 0)))
        preds = preds + ([{"x": 0, "y": 0, "class": "UNKNOWN"}] * (9 - len(preds)))
    elif len(preds) > 9:
        preds = sorted(preds, key=lambda p: p.get("confidence", 0), reverse=True)[:9]
    preds = sorted(preds, key=lambda p: p.get("y", 0))
    rows: List[List[Dict[str, Any]]] = [preds[i:i + 3] for i in range(0, 9, 3)]
    for row in rows:
        row.sort(key=lambda p: p.get("x", 0))
    color_grid: List[List[str]] = [[str(cell.get("class", "UNKNOWN")) for cell in row] for row in rows]
    return color_grid


@app.post("/scan_face")
async def scan_face(
    file: UploadFile = File(...),
    face: str | None = Form(None),
):
    """Concrete endpoint: calls Roboflow Hosted Inference JSON + annotated image.

    Returns: predictions, color_grid, preview (data URL), and saved preview_file path.
    """
    api_key = os.getenv("ROBOFLOW_API_KEY")
    model_id = os.getenv("ROBOFLOW_MODEL_ID", "rubik-s-cube-sticker-detection-rxdj9/4")
    if not api_key:
        return {"error": "ROBOFLOW_API_KEY not set", "roboflow_configured": False}

    content = await file.read()
    filename = file.filename or "image.jpg"
    try:
        # JSON predictions
        json_url = f"https://detect.roboflow.com/{model_id}?api_key={api_key}"
        jresp = requests.post(json_url, files={"file": (filename, content, file.content_type or "image/jpeg")}, timeout=60)
        jresp.raise_for_status()
        result = jresp.json()
        raw_preds = result.get("predictions", [])
        preds = [
            {
                "x": float(p.get("x", 0)),
                "y": float(p.get("y", 0)),
                "confidence": float(p.get("confidence", 0)),
                "class": str(p.get("class", "")),
            }
            for p in raw_preds
        ]
        color_grid = _build_color_grid_from_predictions(preds)

        # Annotated image
        image_url = f"https://detect.roboflow.com/{model_id}?api_key={api_key}&format=image"
        iresp = requests.post(image_url, files={"file": (filename, content, file.content_type or "image/jpeg")}, timeout=60)
        iresp.raise_for_status()
        image_bytes = iresp.content

        out_dir = Path(os.getenv("ROBOFLOW_PREVIEW_DIR", "roboflow_downloads")).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "roboflow_image.jpg"
        with open(out_path, "wb") as f:
            f.write(image_bytes)
        preview_data_url = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"

        return {
            "face": face,
            "predictions": preds,
            "color_grid": color_grid,
            "preview": preview_data_url,
            "preview_file": str(out_path),
            "model_id": model_id,
        }
    except requests.RequestException as e:
        return {"face": face, "error": str(e), "status": getattr(e.response, "status_code", None)}


@app.post("/scan_face_model")
async def scan_face_model(
    file: UploadFile = File(...),
    face: str | None = Form(None),
):
    """Use enhanced cube_processor.py with full error handling and validation from model.py."""
    try:
        # Import our enhanced cube processor with all model.py logic
        import classification.model_api as model_api
        import classification.cube_processor as cube_processor
        
        content = await file.read()
        face_label = face or "U"
        
        # First, get Roboflow detections using model_api
        roboflow_result = model_api.process_single_face(content, face_label)
        
        if not roboflow_result.get("success", False):
            return {"face": face_label, "error": roboflow_result.get("error", "Roboflow processing failed")}
        
        # Now process with cube_processor for validation and state management
        processor_result = cube_processor.process_face(
            predictions=roboflow_result["predictions"], 
            face_label=face_label,
            min_confidence=0.7
        )
        
        # Convert annotated OpenCV image to base64 data URL
        annotated_image = roboflow_result["annotated_image"]
        preview_data_url = model_api.annotated_image_to_base64(annotated_image)
        
        # Save annotated image to file
        out_dir = Path(os.getenv("ROBOFLOW_PREVIEW_DIR", "roboflow_downloads")).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "roboflow_image.jpg"
        
        # Save the annotated image
        annotated_bytes = model_api.annotated_image_to_bytes(annotated_image)
        with open(out_path, "wb") as f:
            f.write(annotated_bytes)
        
        # Get completion status
        completion_status = cube_processor.get_completion_status()
        
        # Enhanced response with cube processor data
        return {
            "face": face_label,
            "success": processor_result["success"],
            "predictions": roboflow_result["predictions"],
            "color_grid": roboflow_result["color_grid"], 
            "preview": preview_data_url,
            "preview_file": str(out_path),
            "detections_count": processor_result.get("detections_count", 0),
            "needs_retake": processor_result.get("needs_retake", False),
            "error": processor_result.get("error"),
            "message": processor_result.get("message"),
            "cube_state": processor_result["cube_state"],
            "face_data": processor_result.get("face_data", []),
            "completion_status": completion_status,
            "source": "cube_processor_with_validation",
        }
    except Exception as e:
        return {"face": face or "unknown", "error": str(e), "success": False}


@app.post("/reset_cube")
async def reset_cube():
    """Reset the global cube state to start scanning a new cube."""
    try:
        import classification.cube_processor as cube_processor
        cube_processor.reset_cube()
        completion_status = cube_processor.get_completion_status()
        
        return {
            "success": True,
            "message": "Cube state reset successfully",
            "cube_state": cube_processor.get_cube_state(),
            "completion_status": completion_status
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/cube_status")
def get_cube_status():
    """Get current cube completion status and state."""
    try:
        import classification.cube_processor as cube_processor
        completion_status = cube_processor.get_completion_status()
        
        return {
            "success": True,
            "cube_state": cube_processor.get_cube_state(),
            "completion_status": completion_status
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/cube_net")
def get_cube_net():
    """Return the current cube net as a dict: { face: 3x3 array }"""
    try:
        import classification.cube_processor as cube_processor
        state = cube_processor.get_cube_state()
        return {"success": True, "cube_net": state}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/cube_net/export")
def export_cube_net():
    """Export the current cube net dict to JSON files in algorithm/ and visualizer/."""
    try:
        import classification.cube_processor as cube_processor
        state = cube_processor.get_cube_state()
        base_dir = Path(__file__).resolve().parent
        out_algo = base_dir / "algorithm" / "cube_net.json"
        out_vis = base_dir / "visualizer" / "cube_net.json"
        out_algo.parent.mkdir(parents=True, exist_ok=True)
        out_vis.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps(state, indent=2)
        out_algo.write_text(content)
        out_vis.write_text(content)
        return {"success": True, "paths": [str(out_algo), str(out_vis)], "bytes": len(content.encode("utf-8"))}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/facelets")
def get_facelets():
    """Return the 54-character facelets string built from the current cube_state."""
    try:
        import classification.cube_processor as cube_processor
        state = cube_processor.get_cube_state()
        facelets = cube_state_to_facelets(state)
        try:
            print("[GET /facelets] state keys:", list(state.keys()) if isinstance(state, dict) else type(state))
            print("[GET /facelets] U face:", state.get("U"))
            print("[GET /facelets] facelets len:", len(facelets))
            print("[GET /facelets] facelets:", facelets)
        except Exception:
            pass
        return {"success": True, "facelets": facelets}
    except Exception as e:
        return {"success": False, "error": str(e), "facelets": ""}


@app.get("/export_txt")
def export_txt():
    """Export the current cube to txt in both algorithm/ and visualizer/ as cube_colors.txt."""
    try:
        import classification.cube_processor as cube_processor
        result = cube_processor.export_cube_data()
        if not result.get("success"):
            # Fallback: force export whatever we have
            result = cube_processor.export_cube_data_force()
            if not result.get("success"):
                return {"success": False, "error": result.get("error", "Export not available")}

        content: str = result.get("file_content", "")
        base_dir = Path(__file__).resolve().parent
        out_algo = base_dir / "algorithm" / "cube_colors.txt"
        out_vis = base_dir / "visualizer" / "cube_colors.txt"

        out_algo.parent.mkdir(parents=True, exist_ok=True)
        out_vis.parent.mkdir(parents=True, exist_ok=True)

        out_algo.write_text(content)
        out_vis.write_text(content)

        return {
            "success": True,
            "paths": [str(out_algo), str(out_vis)],
            "bytes": len(content.encode("utf-8")),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/moves")
def get_moves():
    """Expose moves and moves_made from algorithm.controls for UI/AnimCube."""
    try:
        import algorithm.controls as controls
        data = controls.export_moves()
        return {"success": True, **data}
    except Exception as e:
        return {"success": False, "error": str(e), "moves": [], "moves_made": []}

@app.post("/moves/set")
def set_moves(payload: Dict[str, Any] = Body(...)):
    """Replace moves/moves_made with final results sent from an external script."""
    try:
        import algorithm.controls as controls
        moves_made = payload.get("moves_made")
        moves = payload.get("moves")
        if not isinstance(moves_made, list) or not all(isinstance(x, str) for x in moves_made):
            return {"success": False, "error": "moves_made must be a list[str]"}
        # Replace in-place
        controls.clear_moves()
        controls.moves_made.extend(moves_made)
        if isinstance(moves, list) and all(isinstance(x, str) for x in moves):
            controls.moves.extend(moves)
        else:
            controls.moves.extend(moves_made)
        return {"success": True, "count": len(controls.moves_made)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/moves/clear")
def clear_moves_endpoint():
    try:
        import algorithm.controls as controls
        controls.clear_moves()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/run_algorithm")
def run_algorithm():
    """Run algorithm/main.py as a subprocess; it will POST /moves/set on completion."""
    try:
        base_dir = Path(__file__).resolve().parent
        script = base_dir / "algorithm" / "main.py"
        if not script.exists():
            return {"success": False, "error": f"Not found: {script}"}
        print("[server] /run_algorithm invoked")
        # Use current Python interpreter; run in algorithm/ so relative paths (cube_colors.txt) resolve
        result = subprocess.run([sys.executable, "-u", str(script)], cwd=str(script.parent), capture_output=True, text=True)
        ok = result.returncode == 0
        print(f"[server] /run_algorithm finished rc={result.returncode}")
        return {
            "success": ok,
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:],  # tail for brevity
            "stderr": result.stderr[-2000:],
        }
    except Exception as e:
        print("[server] /run_algorithm error:", e)
        return {"success": False, "error": str(e)}

@app.get("/run_algorithm")
def run_algorithm_get():
    return run_algorithm()


@app.post("/analyze_full")
def analyze_full():
    """Server-driven orchestration: export txt, run algorithm, return moves."""
    try:
        base_dir = Path(__file__).resolve().parent
        # 1) Validate completion
        import classification.cube_processor as cube_processor
        status = cube_processor.get_completion_status()
        if not status.get("is_complete"):
            return {"success": False, "error": "Cube not complete"}

        # 2) Export txt to both locations
        result = cube_processor.export_cube_data()
        if not result.get("success"):
            return {"success": False, "error": result.get("error", "Export failed")}
        content: str = result.get("file_content", "")
        out_algo = (base_dir / "algorithm" / "cube_colors.txt").resolve()
        out_vis = (base_dir / "visualizer" / "cube_colors.txt").resolve()
        out_algo.parent.mkdir(parents=True, exist_ok=True)
        out_vis.parent.mkdir(parents=True, exist_ok=True)
        out_algo.write_text(content)
        out_vis.write_text(content)

        # 3) Run algorithm in its folder
        script = base_dir / "algorithm" / "main.py"
        if not script.exists():
            return {"success": False, "error": f"Not found: {script}"}
        print("[server] /analyze_full: running algorithm/main.py")
        proc = subprocess.run([sys.executable, "-u", str(script)], cwd=str(script.parent), capture_output=True, text=True)
        print(f"[server] /analyze_full: algorithm rc={proc.returncode}")

        # 4) Read moves from controls (set by /moves/set inside main.py) or return stdout for debugging
        try:
            import algorithm.controls as controls
            moves_payload = controls.export_moves()
        except Exception:
            moves_payload = {"moves": [], "moves_made": [], "count": 0}

        return {
            "success": True,
            "export_paths": [str(out_algo), str(out_vis)],
            "returncode": proc.returncode,
            "stdout": proc.stdout[-1500:],
            "stderr": proc.stderr[-1500:],
            "moves": moves_payload.get("moves_made") or moves_payload.get("moves") or [],
            "count": moves_payload.get("count", 0),
        }
    except Exception as e:
        print("[server] /analyze_full error:", e)
        return {"success": False, "error": str(e)}


"use client"
import { useState, useRef, useEffect, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useCube } from "@/contexts/CubeContext"
import { stateToFacelets } from "@/lib/utils"
import { Camera, RotateCcw, Check, Zap, CheckCircle, ArrowRight } from "lucide-react"

interface CameraPageProps {
  onNavigateToVisualizer: () => void
}

export function CameraPage({ onNavigateToVisualizer }: CameraPageProps) {
  const [isCameraActive, setIsCameraActive] = useState(false)
  const [capturedImages, setCapturedImages] = useState<string[]>([])
  const [isVisible, setIsVisible] = useState(false)
  const [cameraError, setCameraError] = useState<string | null>(null)
  const [detections, setDetections] = useState<Record<string, any>>({})
  const facesOrder = ["F", "R", "B", "L", "U", "D"] // Match model.py order
  const [faceIndex, setFaceIndex] = useState(0)
  const currentFace = facesOrder[faceIndex]
  const displayFace = currentFace
  const [cubeState, setCubeState] = useState<any>(null)
  const [completionStatus, setCompletionStatus] = useState<any>(null)
  
  // Face instructions from model.py
  const faceInstructions = {
    F: {
      title: "Front Face",
      instruction: "Hold cube with WHITE center facing camera",
      detail: "BLUE center should face UP"
    },
    R: {
      title: "Right Face", 
      instruction: "Rotate cube 90° left",
      detail: "RED center facing camera, BLUE center UP"
    },
    B: {
      title: "Back Face",
      instruction: "Rotate cube 90° left", 
      detail: "YELLOW center facing camera, BLUE center UP"
    },
    L: {
      title: "Left Face",
      instruction: "Rotate cube 90° left",
      detail: "ORANGE center facing camera, BLUE center UP"
    },
    U: {
      title: "Up Face",
      instruction: "Rotate cube so BLUE center faces camera",
      detail: "YELLOW center should face UP"
    },
    D: {
      title: "Down Face", 
      instruction: "Rotate so GREEN center faces camera",
      detail: "WHITE center should face UP"
    }
  }
  const videoRef = useRef<HTMLVideoElement>(null)
  const { updateMoves, setProcessing, cubeData } = useCube()

  const [pendingPreview, setPendingPreview] = useState<string | null>(null)
  const [pendingDetection, setPendingDetection] = useState<any>(null)
  const [statusMessage, setStatusMessage] = useState<string>("")
  
  // Color mapping for cube visualization
  const getColorStyle = (color: string) => {
    const colorMap: Record<string, string> = {
      'WHITE': 'bg-white border-gray-300',
      'RED': 'bg-red-500 border-red-400',
      'GREEN': 'bg-green-500 border-green-400',
      'BLUE': 'bg-blue-500 border-blue-400',
      'ORANGE': 'bg-orange-500 border-orange-400',
      'YELLOW': 'bg-yellow-400 border-yellow-300',
    }
    return colorMap[color] || 'bg-gray-600 border-gray-500'
  }
  
  // Render a single 3x3 face
  const renderFace = (faceKey: string, faceData?: string[][]) => {
    if (!faceData) {
      return (
        <div className="grid grid-cols-3 gap-1 w-16 h-16">
          {Array.from({ length: 9 }).map((_, i) => (
            <div key={i} className="w-4 h-4 bg-gray-600 border border-gray-500 rounded-sm"></div>
          ))}
        </div>
      )
    }
    
    return (
      <div className="grid grid-cols-3 gap-1 w-16 h-16">
        {faceData.map((row, rowIndex) =>
          row.map((color, colIndex) => (
            <div 
              key={`${rowIndex}-${colIndex}`} 
              className={`w-4 h-4 border rounded-sm ${getColorStyle(color)}`}
              title={color || 'Empty'}
            ></div>
          ))
        )}
      </div>
    )
  }

  function extractVisualizationImage(obj: any): string | null {
    if (!obj) return null
    // If it's a string that looks like a data URL or image URL
    if (typeof obj === "string") {
      const s = obj as string
      if (s.startsWith("data:image")) return s
      if (/^https?:\/\/.*\.(png|jpg|jpeg|webp)(\?.*)?$/i.test(s)) return s
      // Some APIs return raw base64 without prefix
      if (/^[A-Za-z0-9+/=]+$/.test(s) && s.length > 200) {
        return `data:image/jpeg;base64,${s}`
      }
      return null
    }
    // Search common keys first
    const preferredKeys = [
      "visualization",
      "visualization_base64",
      "image",
      "image_base64",
      "output",
      "outputs",
      "plot",
    ]
    for (const k of preferredKeys) {
      if (obj && typeof obj === "object" && obj[k]) {
        const r = extractVisualizationImage(obj[k])
        if (r) return r
      }
    }
    // Fallback: walk the object
    if (Array.isArray(obj)) {
      for (const it of obj) {
        const r = extractVisualizationImage(it)
        if (r) return r
      }
    } else if (typeof obj === "object") {
      for (const key of Object.keys(obj)) {
        const r = extractVisualizationImage(obj[key])
        if (r) return r
      }
    }
    return null
  }

  const handleVideoMetadata = useCallback(() => {
    const video = videoRef.current
    if (!video) return
    // Explicit play after metadata for Safari/iOS
    video.play().catch(() => {})
  }, [])

  useEffect(() => {
    setIsVisible(true)
    // Auto-start camera on mount
    startCamera()
    
    // Initialize cube state from backend
    fetch("http://localhost:8001/cube_status")
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setCubeState(data.cube_state)
          setCompletionStatus(data.completion_status)
          console.log("Loaded cube state:", data)
        }
      })
      .catch(err => console.error("Failed to load cube status:", err))
    
    // Set up periodic stream health check
    const streamCheckInterval = setInterval(() => {
      if (videoRef.current && videoRef.current.srcObject) {
        const video = videoRef.current
        const stream = video.srcObject as MediaStream
        const tracks = stream.getTracks()
        
        // Check if any tracks have ended
        const activeTrack = tracks.find(track => track.readyState === 'live')
        if (!activeTrack) {
          console.log("No active video tracks found, restarting stream...")
          startCamera()
        }
      }
    }, 5000) // Check every 5 seconds
    
    return () => {
      clearInterval(streamCheckInterval)
      stopCamera()
    }
  }, [])

  const startCamera = async () => {
    try {
      setCameraError(null)
      // Try environment camera first; fallback to user/front if not available
      let stream: MediaStream | null = null
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: 1280 },
            height: { ideal: 720 },
            facingMode: { ideal: "environment" },
          },
          audio: false,
        })
      } catch (e) {
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: 1280 },
            height: { ideal: 720 },
            facingMode: { ideal: "user" },
          },
          audio: false,
        })
      }
      // Hide overlay immediately once we have a stream
      if (stream) {
        setIsCameraActive(true)
      }
      if (videoRef.current && stream) {
        const video = videoRef.current
        video.srcObject = stream
        // Ensure autoplay on mobile browsers
        video.muted = true
        video.setAttribute("playsinline", "")
        video.setAttribute("webkit-playsinline", "")
        video.setAttribute("autoplay", "")
        video.setAttribute("muted", "")
        // Overlay already hidden above
        // Attempt to play; retry a few times if needed
        const tryPlay = async (attempt = 0) => {
          try {
            await video.play()
          } catch {
            if (attempt < 5) {
              setTimeout(() => tryPlay(attempt + 1), 300)
            }
          }
        }
        if (video.readyState >= 2) {
          tryPlay()
        } else {
          const onLoaded = () => {
            tryPlay()
            // Also call play explicitly when metadata is loaded
            video.play().catch(() => {})
            video.removeEventListener("loadedmetadata", onLoaded)
          }
          video.addEventListener("loadedmetadata", onLoaded, { once: true } as any)
        }
      }
    } catch (error: any) {
      console.error("Error accessing camera:", error)
      let errorMessage = "Unable to access camera. "

      if (error.name === "NotAllowedError") {
        errorMessage += "Please allow camera permissions and refresh the page."
      } else if (error.name === "NotFoundError") {
        errorMessage += "No camera found on this device."
      } else if (error.name === "NotReadableError") {
        errorMessage += "Camera is being used by another application."
      } else if (error.name === "OverconstrainedError") {
        errorMessage += "Camera doesn't support the required settings."
      } else {
        errorMessage += "Please check your camera permissions and try again."
      }

      setCameraError(errorMessage)
    }
  }

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream
      stream.getTracks().forEach((track) => track.stop())
      videoRef.current.srcObject = null
    }
    setIsCameraActive(false)
  }

  const ensureVideoStream = async () => {
    if (!videoRef.current) return
    
    const video = videoRef.current
    let needsRestart = false
    
    // Check multiple conditions for stream health
    if (!video.srcObject) {
      console.log("Video has no srcObject, restarting...")
      needsRestart = true
    } else {
      const stream = video.srcObject as MediaStream
      const tracks = stream.getTracks()
      const activeTracks = tracks.filter(track => track.readyState === 'live')
      
      if (activeTracks.length === 0) {
        console.log("No active tracks, restarting...")
        needsRestart = true
      } else if (video.paused || video.ended) {
        console.log("Video paused/ended, restarting...")
        needsRestart = true
      } else if (video.videoWidth === 0 || video.videoHeight === 0) {
        console.log("Video has no dimensions, restarting...")
        needsRestart = true
      }
    }
    
    if (needsRestart) {
      // Force camera restart regardless of isCameraActive state
      console.log("Force restarting camera stream...")
      setIsCameraActive(false)
      await startCamera()
    }
  }

  const captureImage = async () => {
    console.log("[CameraPage] captureImage clicked", { isCameraActive, isProcessing: cubeData.isProcessing, face: currentFace })
    setStatusMessage(`Capturing ${currentFace}…`)
    const video = videoRef.current
    if (!video) return

    // Wait for the video to be ready with dimensions
    if (video.readyState < 2) {
      await new Promise((resolve) => {
        const onReady = () => {
          resolve(null)
        }
        video.addEventListener("loadeddata", onReady, { once: true } as any)
      })
    }

    const canvas = document.createElement("canvas")
    const context = canvas.getContext("2d")
    if (!context) return

    const width = video.videoWidth || 1280
    const height = video.videoHeight || 720
    canvas.width = width
    canvas.height = height
    context.drawImage(video, 0, 0, width, height)

    // Helper: convert dataURL to Blob
    const dataUrlToBlob = (dataUrl: string): Blob | null => {
      try {
        const arr = dataUrl.split(',')
        const mime = arr[0].match(/:(.*?);/)?.[1] || 'image/jpeg'
        const bstr = atob(arr[1])
        let n = bstr.length
        const u8arr = new Uint8Array(n)
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n)
        }
        return new Blob([u8arr], { type: mime })
      } catch {
        return null
      }
    }

    // Convert to Blob and send to backend /detect
    const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.85))
    const uploadBlob = blob || dataUrlToBlob(canvas.toDataURL("image/jpeg", 0.85))
    if (!uploadBlob) {
      setCameraError("Failed to capture image from camera.")
      setStatusMessage("Capture failed.")
      return
    }
    try {
      setProcessing(true)
      setStatusMessage("Uploading to /scan_face_model…")
      const form = new FormData()
      form.append("file", uploadBlob, `${currentFace}.jpg`)
      form.append("face", currentFace)
      console.log("[CameraPage] POST /scan_face_model starting")
              const res = await fetch("http://localhost:8001/scan_face_model", { method: "POST", body: form })
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`)
      }
      const data = await res.json()
      console.log("[CameraPage] Enhanced cube processor response", data)
      
      // Update cube state and completion status from enhanced backend IMMEDIATELY
      if (data.cube_state) {
        setCubeState(data.cube_state)
        console.log("✅ Updated cube state:", data.cube_state)
      }
      if (data.completion_status) {
        setCompletionStatus(data.completion_status)
        console.log("✅ Updated completion status:", data.completion_status)
      }
      
      // Handle validation failures (needs_retake)
      if (data.needs_retake) {
        setStatusMessage(`❌ ${data.error || 'Validation failed'} - Please retake.`)
        setCameraError(data.error || 'Detection validation failed')
        return // Don't set pending preview, go straight back to capture
      }
      
      // Handle successful detection
      if (data.success) {
        setStatusMessage(`✅ ${data.message || 'Detection successful'}`)
        // Prefer explicit preview from backend; else search result; else fallback to captured frame
        const viz = data?.preview || extractVisualizationImage(data?.result) || extractVisualizationImage(data)
        const imageDataUrl = viz || canvas.toDataURL("image/jpeg", 0.8)
        // Hold for user confirmation instead of committing immediately
        setPendingPreview(imageDataUrl)
        setPendingDetection(data)
      } else {
        setStatusMessage(`❌ ${data.error || 'Processing failed'}`)
        setCameraError(data.error || 'Face processing failed')
      }
    } catch (e) {
      console.error("[CameraPage] /scan_face_model error", e)
      setCameraError("Failed to upload to Roboflow. Please try again.")
      setStatusMessage("Detection failed.")
    } finally {
      setProcessing(false)
    }
  }

  const confirmPending = async () => {
    if (!pendingPreview || !pendingDetection) return
    // Commit detection to current face and store preview
    setDetections((prev) => ({ ...prev, [currentFace]: pendingDetection }))
    setCapturedImages((prev) => [...prev, pendingPreview])
    setPendingPreview(null)
    setPendingDetection(null)
    
    // Give a moment for React to re-render without overlay, then ensure stream
    setTimeout(async () => {
      await ensureVideoStream()
      // Explicitly try to play the video
      if (videoRef.current) {
        videoRef.current.play().catch(() => {})
      }
    }, 100)
    
    // Advance to next face
    if (faceIndex < facesOrder.length - 1) setFaceIndex((i) => i + 1)
  }

  const retakePending = async () => {
    setPendingPreview(null)
    setPendingDetection(null)
    
    // Give a moment for React to re-render without overlay, then ensure stream
    setTimeout(async () => {
      await ensureVideoStream()
      // Explicitly try to play the video
      if (videoRef.current) {
        videoRef.current.play().catch(() => {})
      }
    }, 100)
  }

  const clearImages = () => {
    setCapturedImages([])
  }
  
  const resetCube = async () => {
    try {
      const response = await fetch("http://localhost:8001/reset_cube", { method: "POST" })
      if (response.ok) {
        const data = await response.json()
        setCubeState(data.cube_state)
        setCompletionStatus(data.completion_status)
        setFaceIndex(0) // Reset to first face
        setCapturedImages([])
        setDetections({})
        setStatusMessage("🔄 Cube reset - starting new scan")
      }
    } catch (e) {
      console.error("Failed to reset cube:", e)
      setStatusMessage("❌ Failed to reset cube")
    }
  }

  const processImages = async () => {
    if (!completionStatus?.is_complete) {
      alert(`Please capture all 6 faces. You have ${completionStatus?.total_faces || 0}/6 completed.`)
      return
    }

    setProcessing(true)
    setStatusMessage("🧠 Analyzing complete cube and generating solution...")

    // Persist current cube position for AnimCube (facelets U,D,F,B,L,R)
    try {
      const COLOR_TO_FACELET: Record<string, string> = {
        WHITE: "w",
        YELLOW: "y",
        ORANGE: "o",
        RED: "r",
        GREEN: "g",
        BLUE: "b",
      }
      // Export facelets in standard AnimCube order U, D, F, B, L, R
      const FACE_ORDER = ["U", "D", "F", "B", "L", "R"] as const
      const toFacelets = (state: any): string => {
        if (!state) return ""
        const out: string[] = []
        for (const f of FACE_ORDER) {
          const grid = state[f]
          for (let r = 0; r < 3; r++) {
            for (let c = 0; c < 3; c++) {
              const color = grid?.[r]?.[c] || ""
              out.push(COLOR_TO_FACELET[color] || "g")
            }
          }
        }
        return out.join("")
      }
      const facelets = stateToFacelets(cubeState)
      if (typeof window !== "undefined") {
        sessionStorage.setItem("animcube_facelets", facelets)
      }
    } catch {}

    await new Promise((resolve) => setTimeout(resolve, 3000))

    // Trigger backend export so the txt lands in algorithm/ and visualizer/
    // Server-driven orchestration: export + run algorithm + return moves
    let loadedMoves: string[] | null = null
    try {
      setStatusMessage("🚀 Analyzing on server…")
      const res = await fetch("http://localhost:8001/analyze_full", { method: "POST" })
      const data = await res.json()
      if (data?.success && Array.isArray(data?.moves) && data.moves.length > 0) {
        loadedMoves = data.moves as string[]
        updateMoves(loadedMoves)
        setStatusMessage(`✅ Loaded ${loadedMoves.length} moves from algorithm`)
      } else {
        setStatusMessage(`⚠️ Analyze returned no moves: ${data?.error || 'unknown'}; using demo sequence`)
        console.log("/analyze_full stdout:", data?.stdout)
        console.log("/analyze_full stderr:", data?.stderr)
      }
    } catch (e) {
      setStatusMessage("⚠️ Failed to run algorithm; using demo sequence")
    }

    // Fallback demo moves if algorithm did not produce any
    if (!loadedMoves) {
      const demo = ["F", "R", "U'", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R", "F'"]
      updateMoves(demo)
    }
    setProcessing(false)
    stopCamera()
    // Redirect to the TSX playground page so it substitutes for the visualizer
    if (typeof window !== "undefined") {
      window.location.href = "/playground"
    } else {
      onNavigateToVisualizer()
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-slate-100 to-blue-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900" />

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-semibold text-slate-900 dark:text-white mb-4 tracking-tight font-poppins">
            Cube Analysis
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Capture high-quality images of your Rubik's cube from multiple angles for precise analysis
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Camera Preview */}
          <Card className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-shadow duration-200">
            <CardHeader className="border-b border-slate-100 dark:border-slate-700 pb-4">
              <CardTitle className="text-slate-900 dark:text-white flex items-center gap-3 text-xl font-medium">
                <div className="p-2 bg-blue-600 rounded-lg">
                  <Camera className="w-5 h-5 text-white" />
                </div>
                Camera Feed
                {isCameraActive && (
                  <div className="flex items-center gap-2 ml-auto">
                    <div className="w-2 h-2 bg-green-500 rounded-full" />
                    <span className="text-sm text-green-600 dark:text-green-400 font-medium">Active</span>
                  </div>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              {/* Face Instructions with Fortune 500 styling */}
              <div className="mb-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
                <div className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">
                  {faceInstructions[displayFace as keyof typeof faceInstructions]?.title} ({displayFace})
                </div>
                <div className="text-sm text-blue-700 dark:text-blue-300 mb-1">
                  {faceInstructions[displayFace as keyof typeof faceInstructions]?.instruction}
                </div>
                <div className="text-xs text-blue-600 dark:text-blue-400">
                  {faceInstructions[displayFace as keyof typeof faceInstructions]?.detail}
                </div>
                {completionStatus && (
                  <div className="mt-2 text-xs text-green-700 dark:text-green-400 font-medium">
                    Progress: {completionStatus.total_faces}/6 faces completed
                  </div>
                )}
              </div>
              {pendingPreview ? (
                <div className="space-y-6">
                  <div className="text-center">
                    <p className="text-slate-600 dark:text-slate-300 font-medium">Review Captured Image</p>
                  </div>
                  <div className="relative">
                    <img
                      src={pendingPreview}
                      alt="Captured cube preview"
                      className="w-full h-80 object-cover rounded-lg border border-slate-200 dark:border-slate-600"
                    />
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className={`w-full h-80 object-cover rounded-lg border border-slate-200 dark:border-slate-600 bg-slate-100 dark:bg-slate-800 ${
                      isCameraActive ? "block" : "hidden"
                    }`}
                  />

                  {!isCameraActive && (
                    <div className="w-full h-80 bg-slate-100 dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-600 flex items-center justify-center">
                      <div className="text-center space-y-4">
                        <Camera className="w-12 h-12 text-slate-400 mx-auto" />
                        <div className="space-y-2">
                          <p className="text-slate-600 dark:text-slate-300 font-medium">
                            {cameraError ? "Camera Unavailable" : "Initializing Camera"}
                          </p>
                          {cameraError && (
                            <p className="text-sm text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
                              {cameraError}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

                {!!statusMessage && (
                  <div className="text-center text-slate-600 dark:text-slate-300 text-sm">{statusMessage}</div>
                )}

              <div className="flex gap-3 justify-center mt-6">
                {!pendingPreview ? (
                  <>
                    <Button
                      onClick={captureImage}
                      className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                      disabled={!isCameraActive || cubeData.isProcessing}
                    >
                      <Camera className="w-4 h-4 mr-2" />
                      Capture
                    </Button>

                    <Button
                      onClick={resetCube}
                      variant="outline"
                      className="px-6 py-2 border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 font-medium rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed bg-transparent"
                      disabled={cubeData.isProcessing}
                    >
                      <RotateCcw className="w-4 h-4 mr-2" />
                      Reset Cube
                    </Button>
                  </>
                ) : (
                  <>
                    <Button
                      onClick={confirmPending}
                      className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200"
                      disabled={cubeData.isProcessing}
                    >
                      <Check className="w-4 h-4 mr-2" />
                      Accept
                    </Button>
                    <Button
                      onClick={retakePending}
                      variant="outline"
                      className="px-6 py-2 border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 font-medium rounded-lg transition-colors duration-200 bg-transparent"
                      disabled={cubeData.isProcessing}
                    >
                      <RotateCcw className="w-4 h-4 mr-2" />
                      Retake
                    </Button>
                  </>
                )}
              </div>

              {/* pending preview moved to right-hand card for clarity */}
            </CardContent>
          </Card>

          {/* Cube Progress & Controls */}
          <Card className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm">
            <CardHeader className="border-b border-slate-100 dark:border-slate-700 pb-4">
              <CardTitle className="text-slate-900 dark:text-white flex items-center gap-3 text-xl font-medium">
                <div className="p-2 bg-slate-600 rounded-lg">
                  <Check className="w-5 h-5 text-white" />
                </div>
                Cube Analysis Progress
                <div className="ml-auto">
                  <span className="px-3 py-1 bg-slate-100 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-md text-slate-700 dark:text-slate-300 font-medium text-sm">
                    {completionStatus?.total_faces || 0} / 6
                  </span>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="space-y-6">
                {/* Cube Net Visualization */}
                {cubeState ? (
                  <div className="bg-slate-50 dark:bg-slate-900/60 rounded-lg p-4 border border-slate-200 dark:border-slate-600">
                  <div className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">
                    Cube Net Visualization
                  </div>
                
                  <div className="grid grid-cols-4 gap-3 w-fit mx-auto justify-items-center items-center">
                    {/* Row 1: U */}
                    <div className="col-start-2 text-center">
                      <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-medium">U</div>
                      {renderFace('U', cubeState.U)}
                    </div>
                
                    {/* Row 2: L, F, R, B */}
                    <div className="col-start-1 text-center">
                      <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-medium">L</div>
                      {renderFace('L', cubeState.L)}
                    </div>
                
                    <div className="col-start-2 text-center">
                      <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-medium">F</div>
                      {renderFace('F', cubeState.F)}
                    </div>
                
                    <div className="col-start-3 text-center">
                      <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-medium">R</div>
                      {renderFace('R', cubeState.R)}
                    </div>
                
                    <div className="col-start-4 text-center">
                      <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-medium">B</div>
                      {renderFace('B', cubeState.B)}
                    </div>
                
                    {/* Row 3: D */}
                    <div className="col-start-2 text-center">
                      <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-medium">D</div>
                      {renderFace('D', cubeState.D)}
                    </div>
                  </div>
                </div>
                ) : (
                  <div className="bg-slate-50 dark:bg-slate-900/60 rounded-lg p-4 border border-slate-200 dark:border-slate-600">
                    <div className="text-center py-8 text-slate-400 dark:text-slate-500">
                      <div className="text-sm">Start capturing faces to see the cube build</div>
                    </div>
                  </div>
                )}
              
                {/* Face Progress Grid */}
                <div className="grid grid-cols-6 gap-2">
                  {facesOrder.map((face, index) => (
                    <div
                      key={face}
                      className={`h-8 flex items-center justify-center rounded text-xs font-bold transition-all ${
                        completionStatus?.completed_faces?.includes(face)
                          ? "bg-emerald-600 text-white"
                          : index === faceIndex
                          ? "bg-blue-600 text-white ring-2 ring-blue-400"
                          : "bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-400"
                      }`}
                    >
                      {face}
                    </div>
                  ))}
                </div>

                {/* Progress Bar */}
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-300">Capture Progress</span>
                    <span className="text-sm text-slate-500 dark:text-slate-400">
                      {Math.round(((completionStatus?.total_faces || 0) / 6) * 100)}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${((completionStatus?.total_faces || 0) / 6) * 100}%` }}
                    />
                  </div>
                </div>
              
                {/* Analyze Button */}
                <Button
                  onClick={processImages}
                  className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={!completionStatus?.is_complete || cubeData.isProcessing}
                >
                  {cubeData.isProcessing ? (
                    <>
                      <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-3"></div>
                      Processing...
                    </>
                  ) : (
                    <>
                      <Zap className="w-4 h-4 mr-3" />
                      Analyze Cube
                    </>
                  )}
                </Button>

                <div className="text-center">
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {completionStatus?.is_complete 
                      ? "All faces captured! Ready to analyze."
                      : "Capture all 6 faces to proceed with analysis"
                    }
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {cubeData.isProcessing && (
          <Card className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm max-w-2xl mx-auto mt-8">
            <CardContent className="pt-8 pb-8">
              <div className="text-center space-y-6">
                <div className="animate-spin w-12 h-12 border-3 border-slate-200 dark:border-slate-700 border-t-blue-600 rounded-full mx-auto"></div>
                <div className="space-y-2">
                  <p className="text-slate-900 dark:text-white font-medium text-lg">Processing Analysis</p>
                  <p className="text-slate-600 dark:text-slate-300">
                    Analyzing {completionStatus?.total_faces || 0} captured faces and computing solution
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

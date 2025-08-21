"use client"
import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useCube } from "@/contexts/CubeContext"
import { Camera, RotateCcw, Check, Zap, CheckCircle, ArrowRight } from "lucide-react"

interface CameraPageProps {
  onNavigateToVisualizer: () => void
}

export function CameraPage({ onNavigateToVisualizer }: CameraPageProps) {
  const [isCameraActive, setIsCameraActive] = useState(false)
  const [capturedImages, setCapturedImages] = useState<string[]>([])
  const [isVisible, setIsVisible] = useState(false)
  const [cameraError, setCameraError] = useState<string | null>(null)
  const [previewImage, setPreviewImage] = useState<string | null>(null)
  const [detections, setDetections] = useState<Record<string, any>>({})
  const [faceIndex, setFaceIndex] = useState(0)
  const [statusMessage, setStatusMessage] = useState<string>("")
  const [processing, setProcessing] = useState(false)
  
  const videoRef = useRef<HTMLVideoElement>(null)
  const { updateMoves, setProcessing: setCubeProcessing, cubeData } = useCube()

  const facesOrder = ["U", "F", "R", "L", "B", "D"]
  const currentFace = facesOrder[faceIndex] || "U"

  useEffect(() => {
    setIsVisible(true)
    startCamera()
    return () => {
      stopCamera()
    }
  }, [])

  const startCamera = async () => {
    try {
      setCameraError(null)
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280, min: 640 },
          height: { ideal: 720, min: 480 },
          facingMode: "environment",
        },
      })
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        videoRef.current.onloadedmetadata = () => {
          videoRef.current
            ?.play()
            .then(() => {
              setIsCameraActive(true)
            })
            .catch((error) => {
              console.error("Error playing video:", error)
              setCameraError("Failed to start video playback. Please try again.")
            })
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

  const captureImage = async () => {
    if (!videoRef.current) return

    setProcessing(true)
    setStatusMessage(`Capturing ${currentFace}...`)

    const canvas = document.createElement("canvas")
    const context = canvas.getContext("2d")
    if (!context) {
      setProcessing(false)
      return
    }

    canvas.width = videoRef.current.videoWidth
    canvas.height = videoRef.current.videoHeight
    context.drawImage(videoRef.current, 0, 0)

    try {
      // Convert to blob and send to Roboflow
      canvas.toBlob(async (blob) => {
        if (!blob) {
          setProcessing(false)
          return
        }

        try {
          setStatusMessage("Uploading to Roboflow...")
          const form = new FormData()
          form.append("file", blob, `${currentFace}.jpg`)
          form.append("face", currentFace)
          
          const res = await fetch("http://localhost:8001/scan_face_model", { 
            method: "POST", 
            body: form 
          })
          
          if (!res.ok) {
            throw new Error(`HTTP ${res.status}`)
          }
          
          const data = await res.json()
          console.log("Roboflow response:", data)
          
          // Get the annotated image from Roboflow
          const roboflowImage = data?.preview
          if (roboflowImage) {
            setPreviewImage(roboflowImage)
            setDetections((prev) => ({ ...prev, [currentFace]: data }))
            setStatusMessage("Detection complete!")
          } else {
            // Fallback to captured frame if no Roboflow image
            const imageDataUrl = canvas.toDataURL("image/jpeg", 0.8)
            setPreviewImage(imageDataUrl)
            setStatusMessage("Using captured image (no detection)")
          }
        } catch (error) {
          console.error("Roboflow error:", error)
          // Fallback to captured frame
          const imageDataUrl = canvas.toDataURL("image/jpeg", 0.8)
          setPreviewImage(imageDataUrl)
          setStatusMessage("Using captured image (detection failed)")
        } finally {
          setProcessing(false)
        }
      }, "image/jpeg", 0.85)
    } catch (error) {
      console.error("Capture error:", error)
      setProcessing(false)
    }
  }

  const approveImage = () => {
    if (previewImage) {
      setCapturedImages((prev) => [...prev, previewImage])
      setPreviewImage(null)
      setStatusMessage("")
      
      // Advance to next face
      if (faceIndex < facesOrder.length - 1) {
        setFaceIndex((i) => i + 1)
      }
      
      // Ensure camera stream is active
      if (videoRef.current && videoRef.current.srcObject) {
        // Camera stream exists, just make sure video is playing
        videoRef.current.play().catch(console.error)
      } else {
        // Restart camera if stream was lost
        startCamera()
      }
    }
  }

  const rejectImage = () => {
    setPreviewImage(null)
    setStatusMessage("")
    
    // Ensure camera stream is active
    if (videoRef.current && videoRef.current.srcObject) {
      // Camera stream exists, just make sure video is playing
      videoRef.current.play().catch(console.error)
    } else {
      // Restart camera if stream was lost
      startCamera()
    }
  }

  const clearImages = () => {
    setCapturedImages([])
    setDetections({})
    setFaceIndex(0)
  }

  const processImages = async () => {
    if (capturedImages.length === 0) {
      alert("Please capture at least one image of your cube first.")
      return
    }

    setCubeProcessing(true)
    await new Promise((resolve) => setTimeout(resolve, 3000))

    const mockMoves = ["F", "R", "U'", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R", "F'"]
    updateMoves(mockMoves)
    setCubeProcessing(false)
    stopCamera()
    onNavigateToVisualizer()
  }

  return (
    <div className="min-h-screen p-4 md:p-8 lg:p-12 relative">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/30 via-transparent to-purple-900/20 pointer-events-none" />

      <div
        className={`max-w-6xl mx-auto space-y-8 relative z-10 transition-all duration-1000 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
      >
        <div className="text-center space-y-4">
          <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold font-[family-name:var(--font-heading)] bg-gradient-to-r from-white via-blue-200 to-blue-400 bg-clip-text text-transparent">
            Cube Detection
          </h1>
          <p className="text-lg md:text-xl text-gray-300 max-w-3xl mx-auto">
            Position your Rubik's cube in the camera view and capture images from different angles
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Camera Preview */}
          <Card className="bg-black/40 border-blue-600/40 backdrop-blur-lg shadow-2xl shadow-blue-500/25 rounded-3xl overflow-hidden">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-3 text-xl font-[family-name:var(--font-heading)]">
                <Camera className="w-6 h-6 text-blue-400" />
                Live Camera Feed
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {previewImage ? (
                <>
                  <div className="text-sm text-blue-200/80">
                    Scanning face: <span className="font-semibold text-blue-100">{currentFace}</span>
                  </div>
                  <div className="relative">
                    <img
                      src={previewImage}
                      alt="Detection preview"
                      className="w-full h-64 md:h-80 object-cover rounded-2xl border-2 border-emerald-500/50 shadow-2xl"
                    />
                  </div>
                  {statusMessage && (
                    <div className="text-blue-300 text-sm text-center">{statusMessage}</div>
                  )}
                  <div className="flex gap-4 justify-center">
                    <Button
                      onClick={approveImage}
                      size="lg"
                      className="px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold shadow-xl transform hover:scale-105 transition-all duration-200 rounded-xl"
                      disabled={processing}
                    >
                      <CheckCircle className="w-5 h-5 mr-2" />
                      Confirm
                    </Button>
                    <Button
                      onClick={rejectImage}
                      variant="outline"
                      size="lg"
                      className="px-8 py-3 border-2 border-gray-500/50 text-gray-300 hover:bg-gray-600 hover:text-white hover:border-gray-600 bg-transparent font-bold transition-all duration-200 rounded-xl"
                      disabled={processing}
                    >
                      <RotateCcw className="w-5 h-5 mr-2" />
                      Retake
                    </Button>
                  </div>
                </>
              ) : (
                <>
                  <div className="text-sm text-blue-200/80">
                    Scanning face: <span className="font-semibold text-blue-100">{currentFace}</span>
                  </div>
                  
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className={`w-full h-64 md:h-80 object-cover rounded-2xl border-2 border-blue-500/40 bg-black shadow-2xl ${
                      isCameraActive ? "block" : "hidden"
                    }`}
                  />

                  {!isCameraActive && (
                    <div className="w-full h-64 md:h-80 bg-gray-800 rounded-2xl border-2 border-blue-500/40 flex items-center justify-center p-6">
                      <div className="text-center space-y-4">
                        <Camera className="w-12 h-12 text-gray-500 mx-auto" />
                        <div className="space-y-2">
                          <p className="text-gray-400 text-lg font-medium">
                            {cameraError ? "Camera Access Issue" : "Starting Camera..."}
                          </p>
                          {cameraError && (
                            <>
                              <p className="text-red-400 text-sm max-w-sm">{cameraError}</p>
                              <Button
                                onClick={startCamera}
                                variant="outline"
                                size="sm"
                                className="mt-3 border-blue-500/50 text-blue-400 hover:bg-blue-600 hover:text-white bg-transparent"
                              >
                                <RotateCcw className="w-4 h-4 mr-2" />
                                Retry Camera Access
                              </Button>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {statusMessage && (
                    <div className="text-blue-300 text-sm text-center">{statusMessage}</div>
                  )}

                  <div className="flex gap-4 justify-center flex-wrap">
                    <Button
                      onClick={captureImage}
                      size="lg"
                      className="px-8 py-3 bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-700 hover:to-green-700 text-white font-bold shadow-xl transform hover:scale-105 transition-all duration-200 rounded-xl focus-ring"
                      disabled={!isCameraActive || processing || cubeData.isProcessing}
                    >
                      {processing ? (
                        <>
                          <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                          Processing...
                        </>
                      ) : (
                        <>
                          <Camera className="w-5 h-5 mr-2" />
                          Capture Image
                        </>
                      )}
                    </Button>

                    <Button
                      onClick={clearImages}
                      variant="outline"
                      size="lg"
                      className="px-6 py-3 border-2 border-orange-500/50 text-orange-400 hover:bg-orange-600 hover:text-white hover:border-orange-600 bg-transparent font-bold transition-all duration-200 rounded-xl focus-ring"
                      disabled={capturedImages.length === 0 || processing || cubeData.isProcessing}
                    >
                      <RotateCcw className="w-5 h-5 mr-2" />
                      Clear All
                    </Button>
                  </div>
                </>
              )}
            </CardContent>
          </Card>

          {/* Captured Images & Controls */}
          <Card className="bg-black/40 border-blue-600/40 backdrop-blur-lg shadow-2xl shadow-blue-500/25 rounded-3xl overflow-hidden">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-3 text-xl font-[family-name:var(--font-heading)]">
                <Check className="w-6 h-6 text-blue-400" />
                Captured Images ({capturedImages.length}/6)
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Face Progress */}
              <div className="grid grid-cols-6 gap-2">
                {facesOrder.map((face, index) => (
                  <div
                    key={face}
                    className={`h-8 flex items-center justify-center rounded text-xs font-bold transition-all ${
                      index < capturedImages.length
                        ? "bg-emerald-600 text-white"
                        : index === faceIndex
                        ? "bg-blue-600 text-white ring-2 ring-blue-400"
                        : "bg-gray-700 text-gray-400"
                    }`}
                  >
                    {face}
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-2 gap-4 max-h-64 overflow-y-auto">
                {capturedImages.map((image, index) => (
                  <div key={index} className="relative">
                    <img
                      src={image}
                      alt={`Face ${facesOrder[index]} captured`}
                      className="w-full h-24 object-cover rounded-lg border border-blue-500/30"
                    />
                    <div className="absolute top-1 right-1 bg-blue-600 text-white text-xs px-2 py-1 rounded">
                      {facesOrder[index]}
                    </div>
                  </div>
                ))}
                {capturedImages.length === 0 && (
                  <div className="col-span-2 text-center py-12 text-gray-400">No images captured yet</div>
                )}
              </div>

              <div className="space-y-4">
                <Button
                  onClick={processImages}
                  size="lg"
                  className="w-full px-8 py-4 text-lg bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 hover:from-blue-700 hover:via-blue-800 hover:to-blue-900 text-white font-bold shadow-2xl shadow-blue-500/40 transform hover:scale-105 transition-all duration-300 rounded-xl focus-ring"
                  disabled={capturedImages.length === 0 || cubeData.isProcessing}
                >
                  {cubeData.isProcessing ? (
                    <>
                      <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-3"></div>
                      Processing Images...
                    </>
                  ) : (
                    <>
                      <Zap className="w-5 h-5 mr-3" />
                      Analyze & Solve Cube
                    </>
                  )}
                </Button>

                <p className="text-sm text-gray-400 text-center">
                  Capture all 6 faces of your cube for complete analysis
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {cubeData.isProcessing && (
          <Card className="bg-black/50 border-blue-600/40 backdrop-blur-lg shadow-2xl shadow-blue-500/25 max-w-2xl mx-auto rounded-3xl animate-fade-in-up">
            <CardContent className="pt-8 pb-8">
              <div className="text-center space-y-6">
                <div className="relative">
                  <div className="animate-spin w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
                  <div className="absolute inset-0 animate-ping w-16 h-16 border-4 border-blue-400/30 rounded-full mx-auto"></div>
                </div>
                <div className="space-y-3">
                  <p className="text-white font-bold text-2xl font-[family-name:var(--font-heading)]">
                    AI Analysis in Progress
                  </p>
                  <p className="text-blue-200 text-lg">
                    Processing {capturedImages.length} image{capturedImages.length !== 1 ? "s" : ""} and computing
                    optimal solution...
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

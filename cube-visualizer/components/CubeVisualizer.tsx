"use client"

import { useEffect, useRef, useState, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"
import { Play, Pause, SkipForward, RotateCcw } from "lucide-react"

interface CubeVisualizerProps {
  moves: string[]
}

export function CubeVisualizer({ moves }: CubeVisualizerProps) {
  const AC_ID = "acjs"
  const cubeContainerRef = useRef<HTMLDivElement>(null)
  const animcubeLoadedRef = useRef(false)
  const playTimerRef = useRef<number | null>(null)
  const faceletsAppliedRef = useRef(false)
  const initializedRef = useRef(false)
  const initialMovesRef = useRef<string>("")
  const initialFaceletsRef = useRef<string>("")
  const cubeInstanceRef = useRef<any>(null)

  const [isPlaying, setIsPlaying] = useState(false)
  const [currentMoveIndex, setCurrentMoveIndex] = useState(0)
  const [speed, setSpeed] = useState([10])

  const getFaceletsFromSession = () => {
    if (typeof window === "undefined") return ""
    return sessionStorage.getItem("animcube_facelets") || ""
  }

  const initializeCube = useCallback(() => {
    if (!cubeContainerRef.current) return
    const w = window as any
    const ac = w?.AnimCube3
    if (!ac) return

    const container = cubeContainerRef.current
    if (!container.id) container.id = AC_ID
    container.innerHTML = ""

    // Per docs: one call with facelets + full move string; let AnimCube handle controls
    if (!initialMovesRef.current) initialMovesRef.current = moves.join(" ")
    if (!initialFaceletsRef.current) initialFaceletsRef.current = getFaceletsFromSession()
    const moveStr = initialMovesRef.current
    const facelets = initialFaceletsRef.current
    // Clean previous listeners per docs to avoid accumulation
    if (w.acjs_removeListeners && w.acjs_removeListeners[container.id]) {
      try { w.acjs_removeListeners[container.id]() } catch {}
    }
    const params = `id=${container.id}&buttonbar=1&counter=1&bgcolor=101020&cubecolor=000000&borderwidth=6&perspective=2${facelets ? `&facelets=${encodeURIComponent(facelets)}` : ""}${moveStr ? `&move=${encodeURIComponent(moveStr)}` : ""}`
    console.log("[CubeVisualizer] init (docs mode)", { moveLen: moves.length, faceletsPresent: !!facelets })
    ac(params)
    faceletsAppliedRef.current = true
    initializedRef.current = true
  }, [moves, currentMoveIndex, speed])

  // Load AnimCube3 with local file or CDN fallback, then initialize
  useEffect(() => {
    const w = window as any
    if (w.AnimCube3) {
      animcubeLoadedRef.current = true
      if (!initializedRef.current) initializeCube()
      return
    }
    if (animcubeLoadedRef.current) return
    const loadWithSrc = (src: string, onFail?: () => void) => {
      const s = document.createElement("script")
      s.src = src
      s.async = true
      s.onload = () => {
        animcubeLoadedRef.current = true
        if (!initializedRef.current) initializeCube()
      }
      s.onerror = () => onFail && onFail()
      document.body.appendChild(s)
    }
    loadWithSrc("/AnimCube3.js", () => loadWithSrc("https://cdn.jsdelivr.net/gh/cubing/AnimCubeJS/AnimCube3.js"))
  }, [initializeCube])

  // Do NOT re-initialize on changes; AnimCube buttonbar controls playback
  useEffect(() => {}, [])

  // Reset move index when moves array changes
  useEffect(() => {
    // In docs mode we let AnimCube handle the playback; no-op here
  }, [moves])

  /**
   * INTEGRATION POINT 2: Implement playback control
   *
   * This handles play/pause functionality. You can:
   * - Use AnimCubeJS built-in controls if available
   * - Implement custom animation timing
   * - Update the cube state based on currentMoveIndex
   */
  const handlePlayPause = useCallback(() => {}, [])

  /**
   * Step forward one move in the sequence
   */
  const handleStepForward = useCallback(() => {}, [])

  /**
   * Reset cube to initial state
   */
  const handleReset = useCallback(() => {}, [])

  const handleSpeedChange = useCallback((newSpeed: number[]) => {
    setSpeed(newSpeed)

    if (isPlaying) {
      if (playTimerRef.current) clearInterval(playTimerRef.current)
      const cube = cubeInstanceRef.current
      if (!cube) return

      const delay = Math.round(60 + (newSpeed[0] - 1) * 36)
      playTimerRef.current = window.setInterval(() => {
        setCurrentMoveIndex((idx) => {
          if (!cube || idx >= moves.length) {
            clearInterval(playTimerRef.current!)
            playTimerRef.current = null
            setIsPlaying(false)
            return idx
          }
          cube.move(moves[idx])
          return idx + 1
        })
      }, delay) as unknown as number
    }
  }, [isPlaying, moves])

  return (
    <div className="w-full max-w-4xl mx-auto bg-black/40 backdrop-blur-sm border border-blue-800/30 rounded-xl shadow-2xl overflow-hidden">
      <div className="relative bg-gradient-to-br from-slate-900 via-blue-900/20 to-slate-900 border-b border-blue-800/30">
        <div ref={cubeContainerRef} className="w-full h-[420px]" />
        {moves.length > 0 && (
          <div className="absolute top-4 right-4 bg-black/60 backdrop-blur-sm border border-blue-800/30 rounded-lg px-4 py-2 text-sm font-medium text-blue-200 shadow-lg">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
              Move {currentMoveIndex} of {moves.length}
            </div>
          </div>
        )}
      </div>
      {/* Sample custom control: Next move (docs-style) */}
      <div className="p-4 bg-slate-900 border-t border-blue-800/30">
        <Button
          onClick={() => {
            const w = window as any
            const id = AC_ID
            try {
              const getVar = w?.acjs_get_var && w.acjs_get_var[id]
              const putVar = w?.acjs_put_var && w.acjs_put_var[id]
              if (getVar && putVar) {
                const mpos = Number(getVar("mpos")) || 0
                const mlen = Number(getVar("mlen")) || 0
                if (mpos < mlen) {
                  putVar("mpos", mpos + 1)
                  setCurrentMoveIndex((v) => Math.min(v + 1, moves.length))
                }
              }
            } catch {}
          }}
          variant="secondary"
          className="bg-blue-600 hover:bg-blue-700 text-white"
        >
          Next
        </Button>
      </div>
    </div>
  )
}
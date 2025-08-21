"use client"

import { useEffect, useRef, useState } from "react"

// Map backend color names to AnimCube facelet letters
const COLOR_TO_FACELET: Record<string, string> = {
  WHITE: "w",
  YELLOW: "y",
  ORANGE: "o",
  RED: "r",
  GREEN: "g",
  BLUE: "b",
}

// Order AnimCube expects for facelets, but our capture has U/D flipped.
// Use D, U, F, B, L, R to correct orientation in the viewer.
const FACE_ORDER = ["D", "U", "F", "B", "L", "R"] as const

function cubeStateToFacelets(cubeState: Record<string, string[][]>): string {
  const out: string[] = []
  for (const face of FACE_ORDER) {
    const grid = cubeState[face]
    if (!grid) continue
    for (let r = 0; r < 3; r++) {
      for (let c = 0; c < 3; c++) {
        const color = grid[r]?.[c] || ""
        out.push(COLOR_TO_FACELET[color] || "g")
      }
    }
  }
  return out.join("")
}

declare global {
  interface Window {
    AnimCube3?: (params: string) => void
    acjs_removeListeners?: Record<string, () => void>
  }
}

export function AnimCubeEmbed() {
  const hostId = "animcube-host"
  const [ready, setReady] = useState(false)
  const hasRunRef = useRef(false)

  useEffect(() => {
    const ensureScript = async () => {
      if (typeof window === "undefined") return
      if (window.AnimCube3) return
      await new Promise<void>((resolve, reject) => {
        const s = document.createElement("script")
        s.src = "/AnimCube3.js"
        s.async = true
        s.onload = () => resolve()
        s.onerror = () => reject(new Error("Failed to load AnimCube3.js"))
        document.body.appendChild(s)
      })
    }

    const run = async () => {
      try {
        await ensureScript()
        let facelets = ""
        // Prefer facelets produced on Analyze
        if (typeof window !== "undefined") {
          facelets = sessionStorage.getItem("animcube_facelets") || ""
        }
        if (!facelets) {
          const res = await fetch("http://localhost:8001/cube_status")
          const data = await res.json()
          facelets = data?.cube_state ? cubeStateToFacelets(data.cube_state) : ""
        }
        if (window.acjs_removeListeners && window.acjs_removeListeners[hostId]) {
          window.acjs_removeListeners[hostId]()
        }
        if (window.AnimCube3) {
          window.AnimCube3(
            `id=${hostId}&facelets=${encodeURIComponent(facelets)}&buttonbar=1&bgcolor=101020&cubecolor=000000&borderwidth=6&perspective=2&speed=10`
          )
          setReady(true)
        }
      } catch (e) {
        console.error("AnimCube init failed", e)
      }
    }

    if (!hasRunRef.current) {
      hasRunRef.current = true
      run()
    } else {
      run()
    }
  }, [])

  return (
    <div
      id={hostId}
      style={{ width: 420, height: 420, margin: "0 auto" }}
      aria-busy={!ready}
    />
  )
}

export default AnimCubeEmbed

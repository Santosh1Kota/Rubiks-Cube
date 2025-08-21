"use client"

import { useEffect, useRef, useState } from "react"

export default function PlaygroundPage() {
  const AC_ID = "acpg"
  const wrapRef = useRef<HTMLDivElement>(null)
  const cubeRef = useRef<HTMLDivElement>(null)
  const toolbarRef = useRef<HTMLDivElement>(null)
  const [ready, setReady] = useState(false)
  const [doneMoves, setDoneMoves] = useState<string[]>([])
  const [originalTokens, setOriginalTokens] = useState<string[]>([])
  const [isPlaying, setIsPlaying] = useState(false)
  const [isFs, setIsFs] = useState(false)
  const [fsSize, setFsSize] = useState<number | null>(null)
  const [zoom, setZoom] = useState<number>(1)
  const idxRef = useRef(0)
  const playingRef = useRef(false)

  // Helpers
  const $ = (id: string): HTMLElement | null => document.getElementById(id)

  // init AnimCube
  useEffect(() => {
    const init = async () => {
      const w: any = window as any
      const el = cubeRef.current
      if (!el) return
      // Ensure direct-access arrays
      w.acjs_removeListeners = w.acjs_removeListeners || []
      w.acjs_move = w.acjs_move || []
      w.acjs_getMove = w.acjs_getMove || []
      w.acjs_startAnimation = w.acjs_startAnimation || []
      w.acjs_pauseAnimation = w.acjs_pauseAnimation || []
      w.acjs_stopAnimation = w.acjs_stopAnimation || []
      w.acjs_clear = w.acjs_clear || []
      w.acjs_get_var = w.acjs_get_var || []
      w.acjs_put_var = w.acjs_put_var || []
      w.acjs_paint = w.acjs_paint || []
      w.acjs_cube = w.acjs_cube || []
      w.acjs_doMove = w.acjs_doMove || []

      el.id = AC_ID
      // Facelets: server-sourced 54-char string
      let facelets = ""
      try {
        const r = await fetch("http://localhost:8001/facelets")
        const d = await r.json()
        facelets = d?.facelets || ""
      } catch {}
      if (!facelets && typeof window !== "undefined") {
        facelets = sessionStorage.getItem("animcube_facelets") || ""
      }
      const load = () => {
        const ac = w.AnimCube3
        if (!ac) return
        try { w.acjs_removeListeners?.[AC_ID]?.() } catch {}
        const params = `id=${AC_ID}&listen=1&buttonbar=0&counter=1&bgcolor=101020&cubecolor=000000&borderwidth=8&perspective=2&align=1&snap=1${facelets ? `&facelets=${encodeURIComponent(facelets)}` : ""}&scale=1`
        ac(params)
        try { el.classList.remove("opacity-0") } catch {}
        setReady(true)
      }
      if (w.AnimCube3) load()
      else {
        const f = document.createElement("script")
        f.src = "https://cdn.jsdelivr.net/gh/cubing/AnimCubeJS/AnimCube3.js"
        f.async = true
        f.onload = load
        f.onerror = () => console.error("[Playground] Failed to load AnimCube3.js from CDN")
        document.body.appendChild(f)
      }

      // Fetch moves like visualizer: prefer moves_made, fallback to moves
      try {
        const r = await fetch("http://localhost:8001/moves")
        const d = await r.json()
        const arr: string[] = d?.moves_made || d?.moves || []
        if (Array.isArray(arr) && arr.length > 0) setOriginalTokens(arr)
        else setOriginalTokens("R U R' U'".split(/\s+/))
        idxRef.current = 0
      } catch {
        setOriginalTokens("R U R' U'".split(/\s+/))
        idxRef.current = 0
      }
    }
    init()
  }, [])

  // fullscreen handler, toolbar move, icon toggle, scale
  useEffect(() => {
    const onFs = () => {
      const ac = wrapRef.current
      const fs = document.fullscreenElement === ac
      const enterI = $("fsEnterIcon")
      const exitI = $("fsExitIcon")
      if (enterI && exitI) {
        if (fs) { enterI.classList.add("hidden"); exitI.classList.remove("hidden") }
        else { exitI.classList.add("hidden"); enterI.classList.remove("hidden") }
      }
      const w: any = window as any
      try {
        w.acjs_put_var?.[AC_ID]?.('scale', fs ? 1.05 : 1, 'n')
        w.acjs_paint?.[AC_ID]?.()
        // eslint-disable-next-line no-console
        console.log('[Playground] fs scale set:', w.acjs_get_var?.[AC_ID]?.('scale'))
      } catch {}
      setZoom(fs ? 1.05 : 1)

      // Move toolbar
      const tb = toolbarRef.current
      if (tb && ac) {
        if (fs) {
          tb.classList.remove("fixed", "inset-x-0", "bottom-0")
          tb.classList.add("absolute", "left-0", "right-0", "bottom-0")
          ac.appendChild(tb)
        } else {
          tb.classList.remove("absolute", "left-0", "right-0", "bottom-0")
          tb.classList.add("fixed", "inset-x-0", "bottom-0")
          document.body.appendChild(tb)
        }
      }
      setIsFs(fs)
      // Recompute available size when fs toggles (avoid stale state)
      requestAnimationFrame(() => updateFsSize(fs))
      try {
        // Prevent page scroll/gestures in fullscreen to avoid passive preventDefault warnings
        document.body.style.overflow = fs ? 'hidden' : ''
      } catch {}
    }
    document.addEventListener("fullscreenchange", onFs)
    return () => document.removeEventListener("fullscreenchange", onFs)
  }, [])

  // compute fullscreen square size and apply it
  const updateFsSize = (fsOverride?: boolean) => {
    const active = fsOverride ?? isFs
    if (!active) { setFsSize(null); return }
    const tb = toolbarRef.current
    const toolbarH = tb ? tb.getBoundingClientRect().height : 0
    const vw = window.innerWidth
    const vh = window.innerHeight
    // Subtract a small margin so the cube never touches/overlaps the toolbar
    const marginPx = 12
    const size = Math.floor(Math.min(vw, Math.max(0, vh - toolbarH - marginPx)))
    setFsSize(size)
    try {
      const w: any = window as any
      // Explicitly tell AnimCube to render at this pixel size in fullscreen
      w.acjs_put_var?.[AC_ID]?.('size', size, 'n')
      w.acjs_paint?.[AC_ID]?.()
    } catch {}
  }

  useEffect(() => {
    if (!isFs) return
    const onR = () => updateFsSize(true)
    window.addEventListener("resize", onR)
    const id = window.setInterval(() => updateFsSize(true), 300)
    updateFsSize(true)
    return () => { window.removeEventListener("resize", onR); window.clearInterval(id) }
  }, [isFs])

  // controls
  const playQueue = () => {
    const w: any = window as any
    if (playingRef.current) return
    if (w?.acjs_get_var?.[AC_ID]?.('animating')) return
    playingRef.current = true
    setIsPlaying(true)
    const next = () => {
      if (!w?.acjs_get_var?.[AC_ID]) return
      if (!playingRef.current) return
      if (idxRef.current >= originalTokens.length) { playingRef.current = false; setIsPlaying(false); return }
      const mv = originalTokens[idxRef.current]
      try {
        if (!w.acjs_move[AC_ID]) w.acjs_move[AC_ID] = []
        const seq = w.acjs_getMove[AC_ID](mv, 0)
        w.acjs_move[AC_ID][0] = seq[0]
        w.acjs_startAnimation[AC_ID](0)
        const t = setInterval(() => {
          const anim = w.acjs_get_var?.[AC_ID]("animating")
          if (!anim) {
            clearInterval(t)
            idxRef.current += 1
            setDoneMoves((d) => (d.length + 1 === idxRef.current ? [...d, mv] : originalTokens.slice(0, idxRef.current)))
            const ms = parseInt((document.getElementById("delay") as HTMLInputElement)?.value || "0", 10) || 0
            if (playingRef.current) setTimeout(next, ms)
            else { setIsPlaying(false) }
          }
        }, 60)
      } catch {}
    }
    next()
  }

  const pause = () => {
    const w: any = window as any
    w.acjs_pauseAnimation?.[AC_ID]?.() || w.acjs_stopAnimation?.[AC_ID]?.()
    playingRef.current = false
    setIsPlaying(false)
  }

  const step = (delta: number) => {
    const w: any = window as any
    try { if (w.acjs_get_var?.[AC_ID]("animating")) w.acjs_stopAnimation?.[AC_ID]?.() } catch {}
    if (delta > 0) {
      if (idxRef.current >= originalTokens.length) return
      const mv = originalTokens[idxRef.current]
      try {
        if (!w.acjs_move[AC_ID]) w.acjs_move[AC_ID] = []
        const seq = w.acjs_getMove[AC_ID](mv, 0)
        w.acjs_move[AC_ID][0] = seq[0]
        w.acjs_startAnimation[AC_ID](0)
        idxRef.current += 1
        setDoneMoves((d) => (d.length + 1 === idxRef.current ? [...d, mv] : originalTokens.slice(0, idxRef.current)))
      } catch {}
    } else if (delta < 0) {
      if (idxRef.current === 0) return
      const prev = originalTokens[idxRef.current - 1]
      const inv = prev.endsWith("2") ? prev : (prev.endsWith("'") ? prev.slice(0,-1) : prev + "'")
      try {
        if (!w.acjs_move[AC_ID]) w.acjs_move[AC_ID] = []
        const seq = w.acjs_getMove[AC_ID](inv, 0)
        w.acjs_move[AC_ID][0] = seq[0]
        w.acjs_startAnimation[AC_ID](0)
        idxRef.current = Math.max(0, idxRef.current - 1)
        setDoneMoves(originalTokens.slice(0, idxRef.current))
      } catch {}
    }
  }

  const reset = () => {
    const w: any = window as any
    try { w.acjs_stopAnimation?.[AC_ID]?.() } catch {}
    try { w.acjs_clear?.[AC_ID]?.() } catch {}
    setDoneMoves([])
    idxRef.current = 0
    playingRef.current = false
    setIsPlaying(false)
  }

  const snap = () => {
    const w: any = window as any
    try {
      const vCopy = w.acjs_vCopy[AC_ID]
      vCopy(w.acjs_eye[AC_ID], w.acjs_initialEye[AC_ID])
      vCopy(w.acjs_eyeX[AC_ID], w.acjs_initialEyeX[AC_ID])
      vCopy(w.acjs_eyeY[AC_ID], w.acjs_initialEyeY[AC_ID])
      w.acjs_paint[AC_ID]()
    } catch {}
  }

  const toggleFs = () => {
    const el = wrapRef.current
    if (!el) return
    if (!document.fullscreenElement) el.requestFullscreen?.()
    else document.exitFullscreen?.()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-black relative">
      <div className="absolute inset-0 bg-gradient-radial from-blue-900/20 via-transparent to-black/40 pointer-events-none" />
      <div className="max-w-6xl mx-auto px-4 pt-6 pb-32">
      <header className="mb-6">
        <h1 className="text-2xl md:text-3xl font-semibold text-white">AnimCube Interactive</h1>
        <p className="text-slate-300 mt-1">Learn patterns step-by-step with a smooth, modern interface.</p>
      </header>

      <main className={`${isFs ? "grid grid-cols-1" : "grid grid-cols-1 lg:grid-cols-3 gap-6"}`}>
        <section className={`${isFs ? "col-span-1" : "lg:col-span-2"}`}>
          <div ref={wrapRef} className={`${isFs ? "fixed inset-0 bg-[#101020] flex items-center justify-center" : "relative rounded-2xl border border-slate-700/60 bg-white/5 backdrop-blur-md shadow-2xl p-4"}`}>
            <div className={`relative ${isFs ? "" : "w-full max-w-[720px] mx-auto aspect-square"} select-none`} style={isFs && fsSize ? { width: fsSize, height: fsSize } : undefined}>
              <div ref={cubeRef} id="acpg" className="absolute inset-0 opacity-0 transition-opacity duration-500"></div>
              <div id="badge" className="absolute top-2 right-2 bg-black/60 border border-blue-700/60 text-blue-100 rounded-md px-3 py-1 text-sm font-medium">Move {doneMoves.length} of {originalTokens.length}</div>
              <button id="fsToggleOverlay" onClick={toggleFs} title="Toggle fullscreen (F)" aria-label="Toggle fullscreen" className="absolute top-2 left-2 bg-black/50 hover:bg-black/60 active:scale-95 transition text-slate-100 border border-slate-700 rounded-full p-2">
                <svg id="fsEnterIcon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M7.69233 18.2781L9.70711 20.2929C9.9931 20.5789 10.0787 21.009 9.92388 21.3827C9.7691 21.7564 9.40446 22 9 22H3C2.44772 22 2 21.5523 2 21V15C2 14.5955 2.24364 14.2309 2.61732 14.0761C2.99099 13.9213 3.42111 14.0069 3.70711 14.2929L5.571 16.1568L9.25289 12.4749C9.64342 12.0844 10.2766 12.0844 10.6671 12.4749L11.3742 13.182C11.7647 13.5725 11.7647 14.2057 11.3742 14.5962L7.69233 18.2781Z" />
                  <path d="M16.3077 5.72187L14.2929 3.70711C14.0069 3.42111 13.9213 2.99099 14.0761 2.61732C14.2309 2.24364 14.5955 2 15 2H21C21.5523 2 22 2.44772 22 3V9C22 9.40446 21.7564 9.7691 21.3827 9.92388C21.009 10.0787 20.5789 9.9931 20.2929 9.70711L18.429 7.84319L14.7471 11.5251C14.3566 11.9156 13.7234 11.9156 13.3329 11.5251L12.6258 10.818C12.2352 10.4275 12.2352 9.7943 12.6258 9.40378L16.3077 5.72187Z" />
                </svg>
                <svg id="fsExitIcon" className="hidden" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M20.04 10.1109L18.0252 8.09612L21.7071 4.41421C22.0976 4.02369 22.0976 3.39052 21.7071 3L21 2.29289C20.6095 1.90237 19.9763 1.90237 19.5858 2.29289L15.9039 5.9748L14.04 4.11089C13.754 3.82489 13.3239 3.73933 12.9502 3.89411C12.5765 4.04889 12.3329 4.41353 12.3329 4.81799V10.818C12.3329 11.3703 12.7806 11.818 13.3329 11.818H19.3329C19.7373 11.818 20.102 11.5744 20.2568 11.2007C20.4115 10.827 20.326 10.3969 20.04 10.1109Z" />
                  <path d="M3.96 13.8891L5.97478 15.9039L2.29289 19.5858C1.90237 19.9763 1.90237 20.6095 2.29289 21L3 21.7071C3.39052 22.0976 4.02369 22.0976 4.41421 21.7071L8.0961 18.0252L9.96 19.8891C10.246 20.1751 10.6761 20.2607 11.0498 20.1059C11.4235 19.9511 11.6671 19.5865 11.6671 19.182V13.182C11.6671 12.6297 11.2194 12.182 10.6671 12.182H4.66711C4.26265 12.182 3.89801 12.4256 3.74323 12.7993C3.58845 13.173 3.674 13.6031 3.96 13.8891Z" />
                </svg>
              </button>
            </div>
          </div>
        </section>
        {!isFs && (
        <aside className="rounded-2xl border border-slate-700/60 bg-white/5 backdrop-blur-md shadow-xl p-4 min-w-[320px]">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-slate-100 font-medium">Move History</h2>
            <span className="text-xs text-blue-200 bg-blue-900/30 border border-blue-800/40 rounded-md px-2 py-0.5">{doneMoves.length} / {originalTokens.length}</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {originalTokens.map((mv, i) => (
              <button key={i} onClick={() => {
                const w: any = window as any
                try { if (w.acjs_get_var?.[AC_ID]('animating')) w.acjs_stopAnimation?.[AC_ID]?.() } catch {}
                try {
                  w.acjs_clear?.[AC_ID]?.()
                  for (let j=0;j<i;j++) {
                    const seq = w.acjs_getMove[AC_ID](originalTokens[j], 0)
                    w.acjs_doMove[AC_ID](w.acjs_cube[AC_ID], seq[0], 0, seq[0].length, false)
                  }
                  w.acjs_paint?.[AC_ID]?.()
                  setDoneMoves(originalTokens.slice(0,i))
                  idxRef.current = i
                  playingRef.current = false
                } catch {}
              }}
                className={`px-3 py-1 rounded-full text-xs border transition ${i < doneMoves.length ? 'bg-blue-600/30 text-blue-100 border-blue-500/40' : i === doneMoves.length ? 'bg-blue-600/50 text-blue-50 border-blue-400/50' : 'bg-slate-900/60 text-slate-200 border-slate-700'}`}
              >{mv}</button>
            ))}
          </div>
          <div className="mt-4 text-xs text-slate-400">Tip: Click a move to jump to that point.</div>
        </aside>
        )}
      </main>

      {/* Bottom toolbar */}
      <div ref={toolbarRef} className="fixed bottom-0 inset-x-0 z-50">
        <div className="mx-auto max-w-6xl px-4 pb-4">
          <div className="rounded-2xl border border-slate-700/60 bg-white/10 backdrop-blur-md shadow-2xl p-3">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <button onClick={playQueue} className="bg-blue-600 hover:bg-blue-700 active:scale-95 transition text-white rounded-md px-4 py-2 shadow">Play</button>
                <button onClick={pause} className="bg-slate-800 hover:bg-slate-700 active:scale-95 transition text-slate-100 rounded-md px-4 py-2 border border-slate-700">Pause</button>
                <button onClick={() => step(-1)} className="bg-slate-800 hover:bg-slate-700 active:scale-95 transition text-slate-100 rounded-md px-4 py-2 border border-slate-700">Prev</button>
                <button onClick={() => step(1)} className="bg-slate-800 hover:bg-slate-700 active:scale-95 transition text-slate-100 rounded-md px-4 py-2 border border-slate-700">Next</button>
                <button onClick={reset} className="bg-slate-800 hover:bg-slate-700 active:scale-95 transition text-slate-100 rounded-md px-4 py-2 border border-slate-700">Reset</button>
                <button onClick={snap} className="bg-slate-800 hover:bg-slate-700 active:scale-95 transition text-slate-100 rounded-md px-4 py-2 border border-slate-700">Snap</button>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <span className="text-slate-300 text-sm">Zoom</span>
                  <input
                    type="range"
                    min={80}
                    max={120}
                    step={1}
                    value={Math.round(zoom * 100)}
                    onChange={(e) => {
                      const v = (parseInt(e.target.value, 10) || 100) / 100
                      setZoom(v)
                      try {
                        const w:any = window as any
                        w.acjs_put_var?.[AC_ID]?.('scale', v, 'n')
                        w.acjs_paint?.[AC_ID]?.()
                        // eslint-disable-next-line no-console
                        console.log('[Playground] zoom scale set:', w.acjs_get_var?.[AC_ID]?.('scale'))
                      } catch {}
                    }}
                    className="accent-blue-500"
                  />
                  <span className="text-blue-200 text-sm">{Math.round(zoom*100)}%</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-slate-300 text-sm">Delay</span>
                  <input type="range" id="delay" min={0} max={3000} step={100} defaultValue={800} className="accent-blue-500" />
                  <span id="delayVal" className="text-blue-200 text-sm">800 ms</span>
                </div>
                {/* Speed control removed per request */}
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  )
}



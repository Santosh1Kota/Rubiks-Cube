"use client"

import { useEffect, useRef, useState } from "react"

export default function TestFaceletsPage() {
  const AC_ID = "ac_test"
  const cubeRef = useRef<HTMLDivElement>(null)
  const [val, setVal] = useState("")
  const [err, setErr] = useState<string>("")

  useEffect(() => {
    const w: any = window as any
    const load = () => {
      // no-op
    }
    if (!w.AnimCube3) {
      const f = document.createElement("script")
      f.src = "https://cdn.jsdelivr.net/gh/cubing/AnimCubeJS/AnimCube3.js"
      f.async = true
      f.onload = load
      document.body.appendChild(f)
    }
  }, [])

  const renderCube = () => {
    const w: any = window as any
    setErr("")
    const s = (val || "").trim()
    if (s.length !== 54) {
      setErr("Facelets must be exactly 54 characters.")
      return
    }
    if (!cubeRef.current || !w.AnimCube3) return
    cubeRef.current.innerHTML = ""
    cubeRef.current.id = AC_ID
    const params = `id=${AC_ID}&listen=0&buttonbar=0&counter=1&bgcolor=101020&cubecolor=000000&borderwidth=8&perspective=2&snap=1&facelets=${encodeURIComponent(s)}&scale=1`
    w.AnimCube3(params)
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <h1 className="text-xl font-semibold mb-4">AnimCube Facelets Tester</h1>
      <div className="flex flex-col gap-3 max-w-2xl">
        <textarea
          className="w-full h-24 p-3 rounded bg-slate-900 border border-slate-700 text-sm font-mono"
          placeholder="Paste 54-char facelets (U,D,F,B,L,R; w,y,o,r,g,b)"
          value={val}
          onChange={(e) => setVal(e.target.value)}
        />
        {err && <div className="text-red-400 text-sm">{err}</div>}
        <div className="flex gap-2">
          <button onClick={renderCube} className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700">Render</button>
          <button onClick={() => { setVal(""); setErr(""); }} className="px-4 py-2 rounded bg-slate-800 border border-slate-700">Clear</button>
        </div>
      </div>
      <div className="mt-6">
        <div ref={cubeRef} className="w-[min(90vw,75vh,800px)] aspect-square bg-black/20 rounded mx-auto" />
      </div>
    </div>
  )
}



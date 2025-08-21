"use client"

import Link from "next/link"
import { useEffect, useRef, useState } from "react"

// Reuse the playground page content inline so we can add site nav
import PlaygroundPage from "../playground/page"

export default function VisualizerPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-black relative">
      <div className="absolute inset-0 bg-gradient-radial from-blue-900/20 via-transparent to-black/40 pointer-events-none" />

      <nav className="sticky top-0 z-50 border-b border-blue-800/30 bg-black/30 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
                <div className="w-4 h-4 bg-white rounded-sm" />
              </div>
              <h1 className="text-2xl font-bold text-white tracking-tight">CubeSolver AI</h1>
            </div>
            <div className="flex space-x-6">
              <Link href="/" className="px-6 py-3 rounded-xl font-medium text-blue-200 hover:text-white hover:bg-blue-800/30 transition">Home</Link>
              <Link href="/camera" className="px-6 py-3 rounded-xl font-medium text-blue-200 hover:text-white hover:bg-blue-800/30 transition">Camera</Link>
              <span className="px-6 py-3 rounded-xl font-medium bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-600/25">Visualizer</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="relative z-10">
        <PlaygroundPage />
      </main>
    </div>
  )
}



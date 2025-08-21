"use client"

import { useState } from "react"
import { HomeInput } from "@/components/HomeInput"
import { CameraPage } from "@/components/CameraPage"
import Link from "next/link"
import { CubeProvider } from "@/contexts/CubeContext"

type Page = "home" | "camera"

export default function Home() {
  const [currentPage, setCurrentPage] = useState<Page>("home")

  return (
    <CubeProvider>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-black relative">
        <div className="absolute inset-0 bg-gradient-radial from-blue-900/20 via-transparent to-black/40 pointer-events-none" />

        <nav className="sticky top-0 z-50 border-b border-blue-800/30 bg-black/30 backdrop-blur-md">
          <div className="max-w-6xl mx-auto px-6 py-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
                  <div className="w-4 h-4 bg-white rounded-sm" />
                </div>
                <h1 className="text-2xl font-bold text-white font-[family-name:var(--font-heading)] tracking-tight">
                  CubeSolver AI
                </h1>
              </div>
              <div className="flex space-x-6">
                <button
                  onClick={() => setCurrentPage("home")}
                  className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 focus-ring ${
                    currentPage === "home"
                      ? "bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-600/25"
                      : "text-blue-200 hover:text-white hover:bg-blue-800/30"
                  }`}
                >
                  Home
                </button>
                <button
                  onClick={() => setCurrentPage("camera")}
                  className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 focus-ring ${
                    currentPage === "camera"
                      ? "bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-600/25"
                      : "text-blue-200 hover:text-white hover:bg-blue-800/30"
                  }`}
                >
                  Camera
                </button>
                <Link href="/visualizer" className="px-6 py-3 rounded-xl font-medium text-blue-200 hover:text-white hover:bg-blue-800/30 transition">
                  Visualizer
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <main className="flex-1 relative z-10">
          {currentPage === "home" && <HomeInput onNavigateToCamera={() => setCurrentPage("camera")} />}
          {currentPage === "camera" && (
            <CameraPage onNavigateToVisualizer={() => { if (typeof window !== "undefined") window.location.href = "/visualizer" }} />
          )}
        </main>
      </div>
    </CubeProvider>
  )
}

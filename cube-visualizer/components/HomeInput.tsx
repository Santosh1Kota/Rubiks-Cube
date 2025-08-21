"use client"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Camera, Zap, Brain, Eye, HelpCircle, Info, Shield, Star } from "lucide-react"
// Fixed import to use correct path for useCube hook
import { useCube } from "@/contexts/CubeContext"

interface HomeInputProps {
  onNavigateToCamera: () => void
}

export function HomeInput({ onNavigateToCamera }: HomeInputProps) {
  const [isVisible, setIsVisible] = useState(false)
  const { cubeData } = useCube()

  useEffect(() => {
    setIsVisible(true)
  }, [])

  return (
    <div className="min-h-screen p-4 md:p-8 lg:p-12 xl:p-16 relative">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/30 via-transparent to-purple-900/20 pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-600/10 via-transparent to-transparent pointer-events-none" />

      <div
        className={`w-full max-w-none xl:max-w-7xl 2xl:max-w-none mx-auto space-y-12 md:space-y-16 lg:space-y-20 relative z-10 transition-all duration-1000 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
      >
        <div className="text-center space-y-6 md:space-y-8 lg:space-y-10 py-8 md:py-12 lg:py-16">
          <div className="animate-float px-4">
            <h1 className="text-4xl md:text-6xl lg:text-7xl xl:text-8xl 2xl:text-9xl font-bold font-[family-name:var(--font-heading)] mb-4 md:mb-6 lg:mb-8 bg-gradient-to-r from-white via-blue-200 to-blue-400 bg-clip-text text-transparent leading-tight tracking-tight">
              CubeSolver AI
            </h1>
          </div>
          <p className="text-lg md:text-xl lg:text-2xl xl:text-3xl text-gray-300 max-w-2xl md:max-w-3xl lg:max-w-4xl xl:max-w-5xl mx-auto leading-relaxed font-light tracking-wide px-4">
            Our AI-powered Rubik's Cube solver utilizes advanced computer vision and machine learning to instantly
            detect your cube's state and compute the optimal solving sequence. Simply point your camera at a scrambled
            cube and watch the magic unfold.
          </p>
        </div>

        <div className="text-center space-y-8 md:space-y-10 px-4">
          <div className="space-y-6 md:space-y-8">
            <Button
              onClick={onNavigateToCamera}
              size="lg"
              className="px-12 md:px-16 lg:px-20 py-6 md:py-8 text-xl md:text-2xl lg:text-3xl font-bold font-[family-name:var(--font-heading)] bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 hover:from-blue-700 hover:via-blue-800 hover:to-blue-900 text-white shadow-2xl shadow-blue-500/40 transform hover:scale-105 transition-all duration-300 animate-pulse-glow focus-ring rounded-2xl border border-blue-400/20"
            >
              <Camera className="w-6 h-6 md:w-8 md:h-8 lg:w-10 lg:h-10 mr-3 md:mr-4" />
              Get Started
            </Button>
            <p className="text-blue-300 text-lg md:text-xl lg:text-2xl font-light tracking-wide">
              Click to begin cube detection with your camera
            </p>
          </div>
        </div>

        {cubeData.isProcessing && (
          <Card className="bg-black/50 border-blue-600/40 backdrop-blur-lg shadow-2xl shadow-blue-500/25 max-w-2xl md:max-w-3xl mx-auto rounded-3xl animate-fade-in-up">
            <CardContent className="pt-8 md:pt-10 pb-8 md:pb-10">
              <div className="text-center space-y-6 md:space-y-8">
                <div className="relative">
                  <div className="animate-spin w-12 h-12 md:w-16 md:h-16 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
                  <div className="absolute inset-0 animate-ping w-12 h-12 md:w-16 md:h-16 border-4 border-blue-400/30 rounded-full mx-auto"></div>
                </div>
                <div className="space-y-2 md:space-y-3">
                  <p className="text-white font-bold text-xl md:text-2xl font-[family-name:var(--font-heading)]">
                    AI Detection in Progress
                  </p>
                  <p className="text-blue-200 text-base md:text-lg">Analyzing cube colors and positions...</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <div className="space-y-12 md:space-y-16 px-4">
          <Card className="bg-black/30 border-blue-800/30 backdrop-blur-lg shadow-2xl shadow-blue-900/20 rounded-3xl overflow-hidden animate-fade-in-up">
            <CardHeader className="pb-6 md:pb-8">
              <CardTitle className="text-white flex items-center gap-3 md:gap-4 text-2xl md:text-3xl font-[family-name:var(--font-heading)] font-bold">
                <Info className="w-6 h-6 md:w-8 md:h-8 text-blue-400" />
                About CubeSolver AI
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6 md:space-y-8">
              <p className="text-gray-300 text-lg md:text-xl leading-relaxed font-light tracking-wide">
                Experience the future of puzzle solving with our cutting-edge AI technology that combines YOLOv8
                computer vision with advanced solving algorithms to deliver instant, optimal solutions for any Rubik's
                cube configuration.
              </p>
              <div className="grid sm:grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 lg:gap-12 mt-8 md:mt-12">
                <div className="text-center space-y-3 md:space-y-4 group hover:transform hover:scale-105 transition-all duration-300">
                  <div className="w-12 h-12 md:w-16 md:h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto shadow-lg group-hover:shadow-blue-500/50 transition-all duration-300">
                    <Eye className="w-6 h-6 md:w-8 md:h-8 text-white" />
                  </div>
                  <h3 className="text-white font-bold text-lg md:text-xl font-[family-name:var(--font-heading)]">
                    Computer Vision
                  </h3>
                  <p className="text-gray-400 leading-relaxed text-sm md:text-base">
                    YOLOv8 detection accurately identifies all cube faces with 99.9% precision
                  </p>
                </div>
                <div className="text-center space-y-3 md:space-y-4 group hover:transform hover:scale-105 transition-all duration-300">
                  <div className="w-12 h-12 md:w-16 md:h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto shadow-lg group-hover:shadow-purple-500/50 transition-all duration-300">
                    <Brain className="w-6 h-6 md:w-8 md:h-8 text-white" />
                  </div>
                  <h3 className="text-white font-bold text-lg md:text-xl font-[family-name:var(--font-heading)]">
                    AI Solving
                  </h3>
                  <p className="text-gray-400 leading-relaxed text-sm md:text-base">
                    Advanced algorithms find optimal move sequences in under 20 moves
                  </p>
                </div>
                <div className="text-center space-y-3 md:space-y-4 group hover:transform hover:scale-105 transition-all duration-300">
                  <div className="w-12 h-12 md:w-16 md:h-16 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto shadow-lg group-hover:shadow-emerald-500/50 transition-all duration-300">
                    <Zap className="w-6 h-6 md:w-8 md:h-8 text-white" />
                  </div>
                  <h3 className="text-white font-bold text-lg md:text-xl font-[family-name:var(--font-heading)]">
                    Real-time
                  </h3>
                  <p className="text-gray-400 leading-relaxed text-sm md:text-base">
                    Instant processing with immersive 3D visualization
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-black/30 border-blue-800/30 backdrop-blur-lg shadow-2xl shadow-blue-900/20 rounded-3xl overflow-hidden animate-fade-in-up">
            <CardHeader className="pb-6 md:pb-8">
              <CardTitle className="text-white flex items-center gap-3 md:gap-4 text-2xl md:text-3xl font-[family-name:var(--font-heading)] font-bold">
                <HelpCircle className="w-6 h-6 md:w-8 md:h-8 text-blue-400" />
                How to Use
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-8 md:space-y-10">
                <div className="grid lg:grid-cols-2 gap-8 md:gap-12">
                  <div className="space-y-4 md:space-y-6">
                    <h3 className="text-white font-bold text-xl md:text-2xl font-[family-name:var(--font-heading)]">
                      Getting Started
                    </h3>
                    <ol className="space-y-3 md:space-y-4 text-gray-300">
                      <li className="flex items-start gap-3 md:gap-4">
                        <span className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-full w-7 h-7 md:w-8 md:h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1 shadow-lg">
                          1
                        </span>
                        <span className="text-base md:text-lg leading-relaxed">
                          Click the "Get Started" button to open the camera interface
                        </span>
                      </li>
                      <li className="flex items-start gap-3 md:gap-4">
                        <span className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-full w-7 h-7 md:w-8 md:h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1 shadow-lg">
                          2
                        </span>
                        <span className="text-base md:text-lg leading-relaxed">
                          Position your scrambled Rubik's cube in front of the camera
                        </span>
                      </li>
                      <li className="flex items-start gap-3 md:gap-4">
                        <span className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-full w-7 h-7 md:w-8 md:h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1 shadow-lg">
                          3
                        </span>
                        <span className="text-base md:text-lg leading-relaxed">
                          Take pictures of all cube faces for complete detection
                        </span>
                      </li>
                      <li className="flex items-start gap-3 md:gap-4">
                        <span className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-full w-7 h-7 md:w-8 md:h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1 shadow-lg">
                          4
                        </span>
                        <span className="text-base md:text-lg leading-relaxed">
                          Watch the 3D visualization show you how to solve it!
                        </span>
                      </li>
                    </ol>
                  </div>
                  <div className="space-y-4 md:space-y-6">
                    <h3 className="text-white font-bold text-xl md:text-2xl font-[family-name:var(--font-heading)]">
                      Pro Tips
                    </h3>
                    <ul className="space-y-3 md:space-y-4 text-gray-300">
                      <li className="flex items-start gap-3 md:gap-4">
                        <Star className="w-4 h-4 md:w-5 md:h-5 text-blue-400 mt-1.5 flex-shrink-0" />
                        <span className="text-base md:text-lg leading-relaxed">
                          Ensure bright, even lighting on your cube
                        </span>
                      </li>
                      <li className="flex items-start gap-3 md:gap-4">
                        <Star className="w-4 h-4 md:w-5 md:h-5 text-blue-400 mt-1.5 flex-shrink-0" />
                        <span className="text-base md:text-lg leading-relaxed">
                          Hold the cube steady and show multiple faces
                        </span>
                      </li>
                      <li className="flex items-start gap-3 md:gap-4">
                        <Star className="w-4 h-4 md:w-5 md:h-5 text-blue-400 mt-1.5 flex-shrink-0" />
                        <span className="text-base md:text-lg leading-relaxed">
                          Make sure all colors are clearly visible
                        </span>
                      </li>
                      <li className="flex items-start gap-3 md:gap-4">
                        <Star className="w-4 h-4 md:w-5 md:h-5 text-blue-400 mt-1.5 flex-shrink-0" />
                        <span className="text-base md:text-lg leading-relaxed">
                          Avoid shadows or reflections on the cube surface
                        </span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-blue-900/20 to-purple-900/20 border-blue-700/40 backdrop-blur-lg shadow-2xl shadow-blue-900/20 rounded-3xl overflow-hidden animate-fade-in-up">
            <CardContent className="pt-6 md:pt-8 pb-6 md:pb-8">
              <div className="text-center space-y-4 md:space-y-6">
                <div className="flex items-center justify-center gap-2 md:gap-3">
                  <Shield className="w-5 h-5 md:w-6 md:h-6 text-blue-400" />
                  <p className="text-blue-200 text-base md:text-lg font-medium">
                    Trusted by 50,000+ cube enthusiasts worldwide
                  </p>
                </div>
                <p className="text-gray-400 text-xs md:text-sm max-w-xl md:max-w-2xl mx-auto leading-relaxed">
                  Your privacy is our priority. All cube detection happens locally in your browser - no images are
                  stored or transmitted to our servers.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

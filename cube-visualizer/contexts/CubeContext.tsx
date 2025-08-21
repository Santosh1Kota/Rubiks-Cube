"use client"

import { createContext, useContext, useState, type ReactNode } from "react"

interface CubeState {
  moves: string[]
  cubeState?: string // Optional cube state representation
  isProcessing: boolean
}

interface CubeContextType {
  cubeData: CubeState
  setCubeData: (data: Partial<CubeState>) => void
  updateMoves: (moves: string[]) => void
  setProcessing: (processing: boolean) => void
}

const CubeContext = createContext<CubeContextType | undefined>(undefined)

export function CubeProvider({ children }: { children: ReactNode }) {
  const [cubeData, setCubeDataState] = useState<CubeState>({
    moves: [],
    isProcessing: false,
  })

  const setCubeData = (data: Partial<CubeState>) => {
    setCubeDataState((prev) => ({ ...prev, ...data }))
  }

  const updateMoves = (moves: string[]) => {
    setCubeData({ moves })
  }

  const setProcessing = (processing: boolean) => {
    setCubeData({ isProcessing: processing })
  }

  return (
    <CubeContext.Provider value={{ cubeData, setCubeData, updateMoves, setProcessing }}>
      {children}
    </CubeContext.Provider>
  )
}

export function useCube() {
  const context = useContext(CubeContext)
  if (context === undefined) {
    throw new Error("useCube must be used within a CubeProvider")
  }
  return context
}

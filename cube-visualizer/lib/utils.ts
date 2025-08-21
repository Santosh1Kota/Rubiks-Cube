import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export type CubeState = Record<string, string[][]>

const COLOR_TO_FACELET: Record<string, string> = {
  WHITE: "w",
  YELLOW: "y",
  ORANGE: "o",
  RED: "r",
  GREEN: "g",
  BLUE: "b",
}

function flipRows(grid: string[][]): string[][] {
  return grid.map((row) => [...row].reverse())
}

function rotate90cw(grid: string[][]): string[][] {
  const n = grid.length
  const res: string[][] = Array.from({ length: n }, () => Array(n).fill(""))
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      res[c][n - 1 - r] = grid[r][c]
    }
  }
  return res
}

function rotate180(grid: string[][]): string[][] {
  return rotate90cw(rotate90cw(grid))
}

function transformFaceForAnimCube(face: string, gridIn: string[][]): string[][] {
  if (!Array.isArray(gridIn)) return gridIn
  // Deep copy
  let grid = gridIn.map((row) => row.slice())
  // Common vertical mirror as used elsewhere
  grid = grid.slice().reverse()
  if (face === "F") {
    grid = flipRows(grid)
  } else if (face === "L") {
    grid = rotate90cw(grid)
  } else if (face === "B") {
    grid = rotate180(grid)
    grid = flipRows(grid)
  } else if (face === "D") {
    grid = rotate180(grid)
  } else if (face === "R") {
    grid = rotate180(grid)
    grid = rotate90cw(grid)
  } else if (face === "U") {
    grid = rotate90cw(grid)
  }
  return grid
}

export function stateToFacelets(cubeState: CubeState | undefined | null): string {
  if (!cubeState) return ""
  const FACE_ORDER: Array<keyof CubeState> = ["U", "D", "F", "B", "L", "R"]
  const out: string[] = []
  for (const f of FACE_ORDER) {
    const grid = (cubeState as any)[f]
    for (let r = 0; r < 3; r++) {
      for (let c = 0; c < 3; c++) {
        const color = grid?.[r]?.[c] || ""
        out.push(COLOR_TO_FACELET[color] || "g")
      }
    }
  }
  return out.join("")
}

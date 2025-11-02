import { useState, useEffect, useCallback } from 'react'
import useInterval from './useInterval'
import { randomTetromino } from './tetrominos'
import './App.css'

const ROWS = 20
const COLS = 10

function createBoard() {
  return Array.from({ length: ROWS }, () => Array(COLS).fill(null))
}

function canMove(board, shape, pos) {
  for (let r = 0; r < shape.length; r++) {
    for (let c = 0; c < shape[r].length; c++) {
      if (shape[r][c]) {
        const x = pos.x + c
        const y = pos.y + r
        if (x < 0 || x >= COLS || y >= ROWS) return false
        if (y >= 0 && board[y][x]) return false
      }
    }
  }
  return true
}

function merge(board, shape, pos, color) {
  const newBoard = board.map(row => row.slice())
  for (let r = 0; r < shape.length; r++) {
    for (let c = 0; c < shape[r].length; c++) {
      if (shape[r][c]) {
        const x = pos.x + c
        const y = pos.y + r
        if (y >= 0) newBoard[y][x] = color
      }
    }
  }
  return newBoard
}

function clearLines(board) {
  const newBoard = board.filter(row => row.some(cell => !cell))
  const cleared = ROWS - newBoard.length
  while (newBoard.length < ROWS) newBoard.unshift(Array(COLS).fill(null))
  return { board: newBoard, cleared }
}

function App() {
  const [board, setBoard] = useState(createBoard())
  const [piece, setPiece] = useState(() => randomTetromino())
  const [pos, setPos] = useState({ x: 3, y: -2 })
  const [rotation, setRotation] = useState(0)
  const [gameOver, setGameOver] = useState(false)
  const [score, setScore] = useState(0)

  const shape = piece.shape[rotation % piece.shape.length]

  const drop = useCallback(() => {
    const newPos = { x: pos.x, y: pos.y + 1 }
    if (canMove(board, shape, newPos)) {
      setPos(newPos)
    } else {
      const merged = merge(board, shape, pos, piece.color)
      const { board: clearedBoard, cleared } = clearLines(merged)
      setBoard(clearedBoard)
      if (cleared) setScore(s => s + cleared * 100)
      const nextPiece = randomTetromino()
      const startPos = { x: 3, y: -2 }
      if (!canMove(clearedBoard, nextPiece.shape[0], startPos)) {
        setGameOver(true)
        return
      }
      setPiece(nextPiece)
      setRotation(0)
      setPos(startPos)
    }
  }, [board, shape, pos, piece])

  useInterval(() => {
    if (!gameOver) drop()
  }, 500)

  const move = (dx) => {
    const newPos = { x: pos.x + dx, y: pos.y }
    if (canMove(board, shape, newPos)) setPos(newPos)
  }

  const rotate = () => {
    const newRot = (rotation + 1) % piece.shape.length
    const newShape = piece.shape[newRot]
    if (canMove(board, newShape, pos)) setRotation(newRot)
  }

  useEffect(() => {
    const handleKey = (e) => {
      if (gameOver) return
      if (e.key === 'ArrowLeft') move(-1)
      if (e.key === 'ArrowRight') move(1)
      if (e.key === 'ArrowDown') drop()
      if (e.key === 'ArrowUp') rotate()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [move, drop, rotate, gameOver])

  const cells = merge(board, shape, pos, piece.color)

  return (
    <div className="tetris">
      <h1>Tetris</h1>
      <p>Score: {score}</p>
      {gameOver && <p className="game-over">Game Over</p>}
      <div className="board">
        {cells.map((row, r) => (
          <div key={r} className="row">
            {row.map((cell, c) => (
              <div key={c} className="cell" style={{ background: cell || '#111' }} />
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}

export default App

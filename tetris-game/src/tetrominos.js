export const TETROMINOS = {
  I: {
    shape: [
      [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
      [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]],
    ],
    color: 'cyan',
  },
  J: {
    shape: [
      [[1,0,0],[1,1,1],[0,0,0]],
      [[0,1,1],[0,1,0],[0,1,0]],
      [[0,0,0],[1,1,1],[0,0,1]],
      [[0,1,0],[0,1,0],[1,1,0]],
    ],
    color: 'blue',
  },
  L: {
    shape: [
      [[0,0,1],[1,1,1],[0,0,0]],
      [[0,1,0],[0,1,0],[0,1,1]],
      [[0,0,0],[1,1,1],[1,0,0]],
      [[1,1,0],[0,1,0],[0,1,0]],
    ],
    color: 'orange',
  },
  O: {
    shape: [
      [[1,1],[1,1]],
    ],
    color: 'yellow',
  },
  S: {
    shape: [
      [[0,1,1],[1,1,0],[0,0,0]],
      [[0,1,0],[0,1,1],[0,0,1]],
    ],
    color: 'green',
  },
  T: {
    shape: [
      [[0,1,0],[1,1,1],[0,0,0]],
      [[0,1,0],[0,1,1],[0,1,0]],
      [[0,0,0],[1,1,1],[0,1,0]],
      [[0,1,0],[1,1,0],[0,1,0]],
    ],
    color: 'purple',
  },
  Z: {
    shape: [
      [[1,1,0],[0,1,1],[0,0,0]],
      [[0,0,1],[0,1,1],[0,1,0]],
    ],
    color: 'red',
  },
}

export const RANDOM_TETROMINOS = ['I','J','L','O','S','T','Z']

export function randomTetromino() {
  const keys = RANDOM_TETROMINOS
  const rand = keys[Math.floor(Math.random()*keys.length)]
  return TETROMINOS[rand]
}

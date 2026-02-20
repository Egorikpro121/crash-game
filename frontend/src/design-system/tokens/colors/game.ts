/**
 * Game-specific colors
 * Multipliers, crash, bets
 */

export const gameColors = {
  // Multiplier colors (gradient based on value)
  multiplier: {
    low: '#4caf50',      // 1.00x - 2.00x (green)
    medium: '#ffc107',   // 2.00x - 5.00x (yellow)
    high: '#ff9800',     // 5.00x - 10.00x (orange)
    veryHigh: '#ff3333', // 10.00x+ (red)
  },
  
  // Crash colors
  crash: {
    background: '#ff3333',
    text: '#ffffff',
    glow: 'rgba(255, 51, 51, 0.5)',
  },
  
  // Bet colors
  bet: {
    active: '#0088cc',
    won: '#00d4aa',
    lost: '#ff3333',
    pending: '#ffc107',
  },
  
  // Chart colors
  chart: {
    line: '#0088cc',
    area: 'rgba(0, 136, 204, 0.2)',
    grid: '#2d2d2d',
    crash: '#ff3333',
  },
  
  // Player colors
  player: {
    you: '#0088cc',
    others: '#808080',
    top: '#ffd700',
  },
} as const;

export type GameColors = typeof gameColors;

/**
 * Gradient definitions
 */

export const gradients = {
  primary: 'linear-gradient(135deg, #0088cc 0%, #00d4aa 100%)',
  secondary: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)',
  success: 'linear-gradient(135deg, #00d4aa 0%, #00b894 100%)',
  error: 'linear-gradient(135deg, #ff3333 0%, #c62828 100%)',
  multiplier: {
    low: 'linear-gradient(135deg, #4caf50 0%, #00d4aa 100%)',
    medium: 'linear-gradient(135deg, #ffc107 0%, #ff9800 100%)',
    high: 'linear-gradient(135deg, #ff9800 0%, #ff3333 100%)',
    veryHigh: 'linear-gradient(135deg, #ff3333 0%, #c62828 100%)',
  },
  background: 'linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%)',
  neomorphic: 'linear-gradient(145deg, #2d2d2d 0%, #1a1a1a 100%)',
} as const;

export type Gradients = typeof gradients;

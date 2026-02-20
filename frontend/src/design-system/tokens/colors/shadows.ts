/**
 * Shadow colors for Neomorphism
 * Used for creating depth and 3D effects
 */

export const shadowColors = {
  // Light shadows (for inset effects)
  light: {
    soft: 'rgba(255, 255, 255, 0.05)',
    medium: 'rgba(255, 255, 255, 0.08)',
    hard: 'rgba(255, 255, 255, 0.12)',
  },
  
  // Dark shadows (for outset effects)
  dark: {
    soft: 'rgba(0, 0, 0, 0.3)',
    medium: 'rgba(0, 0, 0, 0.4)',
    hard: 'rgba(0, 0, 0, 0.5)',
  },
  
  // Colored shadows
  colored: {
    primary: 'rgba(0, 136, 204, 0.3)',
    success: 'rgba(0, 212, 170, 0.3)',
    error: 'rgba(255, 51, 51, 0.3)',
    warning: 'rgba(255, 152, 0, 0.3)',
  },
} as const;

export type ShadowColors = typeof shadowColors;

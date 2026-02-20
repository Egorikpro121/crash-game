/**
 * Multiplier-specific design tokens
 */

import { gameColors } from '../colors/game';
import { typography } from '../typography';

export const multiplierTokens = {
  // Colors based on multiplier value
  colors: {
    low: gameColors.multiplier.low,        // 1.00x - 2.00x
    medium: gameColors.multiplier.medium,  // 2.00x - 5.00x
    high: gameColors.multiplier.high,      // 5.00x - 10.00x
    veryHigh: gameColors.multiplier.veryHigh, // 10.00x+
  },
  
  // Typography for multiplier display
  typography: {
    small: typography.styles.h3,
    medium: typography.styles.h2,
    large: typography.styles.h1,
    display: typography.styles.display,
  },
  
  // Animation settings
  animation: {
    updateDuration: 100, // ms
    pulseDuration: 2000, // ms
  },
} as const;

export type MultiplierTokens = typeof multiplierTokens;

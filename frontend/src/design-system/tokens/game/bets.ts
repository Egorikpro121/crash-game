/**
 * Bet-specific design tokens
 */

import { gameColors } from '../colors/game';
import { shadows } from '../shadows';

export const betTokens = {
  colors: {
    active: gameColors.bet.active,
    won: gameColors.bet.won,
    lost: gameColors.bet.lost,
    pending: gameColors.bet.pending,
  },
  
  shadows: {
    active: shadows.neomorphic.colored.primary,
    won: shadows.neomorphic.colored.success,
    lost: shadows.neomorphic.colored.error,
  },
  
  sizes: {
    min: 0.01,
    max: 100,
    step: 0.01,
  },
} as const;

export type BetTokens = typeof betTokens;

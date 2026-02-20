/**
 * Crash-specific design tokens
 */

import { gameColors } from '../colors/game';
import { shadows } from '../shadows';

export const crashTokens = {
  colors: {
    background: gameColors.crash.background,
    text: gameColors.crash.text,
    glow: gameColors.crash.glow,
  },
  
  shadows: {
    glow: `0 0 20px ${gameColors.crash.glow}, 0 0 40px ${gameColors.crash.glow}`,
    intense: `0 0 30px ${gameColors.crash.glow}, 0 0 60px ${gameColors.crash.glow}`,
  },
  
  animation: {
    duration: 500, // ms
    easing: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
} as const;

export type CrashTokens = typeof crashTokens;

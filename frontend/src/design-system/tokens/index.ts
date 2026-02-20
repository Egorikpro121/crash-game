/**
 * Design tokens - Main export
 * Centralized export of all design tokens
 */

export * from './colors';
export * from './typography';
export * from './spacing';
export * from './shadows';
export * from './radius';
export * from './zIndex';
export * from './breakpoints';
export * from './animation';
export * from './game';

import { colors } from './colors';
import { typography } from './typography';
import { spacingTokens } from './spacing';
import { shadows } from './shadows';
import { radiusTokens } from './radius';
import { zIndexTokens } from './zIndex';
import { breakpointTokens } from './breakpoints';
import { animation } from './animation';
import { gameTokens } from './game';

export const tokens = {
  colors,
  typography,
  spacing: spacingTokens,
  shadows,
  radius: radiusTokens,
  zIndex: zIndexTokens,
  breakpoints: breakpointTokens,
  animation,
  game: gameTokens,
} as const;

export type Tokens = typeof tokens;

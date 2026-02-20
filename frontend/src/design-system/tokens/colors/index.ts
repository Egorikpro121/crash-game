/**
 * Color tokens export
 * Centralized color system for the design system
 */

export * from './primary';
export * from './neutral';
export * from './semantic';
export * from './game';
export * from './gradients';
export * from './shadows';

import { primaryColors } from './primary';
import { neutralColors } from './neutral';
import { semanticColors } from './semantic';
import { gameColors } from './game';
import { gradients } from './gradients';
import { shadowColors } from './shadows';

export const colors = {
  primary: primaryColors,
  neutral: neutralColors,
  semantic: semanticColors,
  game: gameColors,
  gradients,
  shadows: shadowColors,
} as const;

export type Colors = typeof colors;

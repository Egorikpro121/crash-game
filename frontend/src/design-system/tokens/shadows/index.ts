/**
 * Shadow tokens export
 */

export * from './light';
export * from './dark';
export * from './elevations';
export * from './neomorphic';

import { lightShadows } from './light';
import { darkShadows } from './dark';
import { elevations } from './elevations';
import { neomorphicShadows } from './neomorphic';

export const shadows = {
  light: lightShadows,
  dark: darkShadows,
  elevations,
  neomorphic: neomorphicShadows,
} as const;

export type Shadows = typeof shadows;

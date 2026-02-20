/**
 * Breakpoint tokens export
 */

export * from './sizes';
export * from './media';

import { breakpoints } from './sizes';
import { media } from './media';

export const breakpointTokens = {
  sizes: breakpoints,
  media,
} as const;

export type BreakpointTokens = typeof breakpointTokens;

/**
 * Animation durations
 * In milliseconds
 */

export const durations = {
  instant: 0,
  fast: 100,
  normal: 200,
  slow: 300,
  slower: 500,
  slowest: 1000,
} as const;

export type Durations = typeof durations;

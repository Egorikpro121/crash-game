/**
 * Animation delays
 * In milliseconds
 */

export const delays = {
  none: 0,
  short: 50,
  medium: 100,
  long: 200,
  longer: 300,
} as const;

export type Delays = typeof delays;

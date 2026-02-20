/**
 * Animation tokens export
 */

export * from './durations';
export * from './easings';
export * from './delays';

import { durations } from './durations';
import { easings } from './easings';
import { delays } from './delays';

export const animation = {
  durations,
  easings,
  delays,
} as const;

export type Animation = typeof animation;

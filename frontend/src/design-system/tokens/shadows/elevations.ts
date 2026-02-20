/**
 * Elevation shadows
 * Different levels of depth (0-5)
 */

import { shadowColors } from '../colors/shadows';

export const elevations = {
  0: 'none',
  1: `1px 1px 2px ${shadowColors.dark.soft}, -1px -1px 2px ${shadowColors.light.soft}`,
  2: `2px 2px 4px ${shadowColors.dark.soft}, -2px -2px 4px ${shadowColors.light.soft}`,
  3: `4px 4px 8px ${shadowColors.dark.medium}, -4px -4px 8px ${shadowColors.light.medium}`,
  4: `6px 6px 12px ${shadowColors.dark.medium}, -6px -6px 12px ${shadowColors.light.medium}`,
  5: `8px 8px 16px ${shadowColors.dark.hard}, -8px -8px 16px ${shadowColors.light.hard}`,
} as const;

export type Elevations = typeof elevations;

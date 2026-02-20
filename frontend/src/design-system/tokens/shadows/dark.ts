/**
 * Dark shadows (outset effects)
 * For creating raised/outward appearance
 */

import { shadowColors } from '../colors/shadows';

export const darkShadows = {
  // Outset shadows (raised effect)
  outset: {
    soft: `2px 2px 4px ${shadowColors.dark.soft}, -2px -2px 4px ${shadowColors.light.soft}`,
    medium: `4px 4px 8px ${shadowColors.dark.medium}, -4px -4px 8px ${shadowColors.light.medium}`,
    hard: `6px 6px 12px ${shadowColors.dark.hard}, -6px -6px 12px ${shadowColors.light.hard}`,
  },
  
  // Single direction outset
  outsetTop: `0 -2px 4px ${shadowColors.dark.soft}`,
  outsetBottom: `0 2px 4px ${shadowColors.dark.soft}`,
  outsetLeft: `-2px 0 4px ${shadowColors.dark.soft}`,
  outsetRight: `2px 0 4px ${shadowColors.dark.soft}`,
} as const;

export type DarkShadows = typeof darkShadows;

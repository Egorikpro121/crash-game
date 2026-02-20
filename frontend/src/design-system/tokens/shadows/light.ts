/**
 * Light shadows (inset effects)
 * For creating pressed/inward appearance
 */

import { shadowColors } from '../colors/shadows';

export const lightShadows = {
  // Inset shadows (pressed effect)
  inset: {
    soft: `inset 2px 2px 4px ${shadowColors.light.soft}, inset -2px -2px 4px ${shadowColors.dark.soft}`,
    medium: `inset 4px 4px 8px ${shadowColors.light.medium}, inset -4px -4px 8px ${shadowColors.dark.medium}`,
    hard: `inset 6px 6px 12px ${shadowColors.light.hard}, inset -6px -6px 12px ${shadowColors.dark.hard}`,
  },
  
  // Single direction inset
  insetTop: `inset 0 2px 4px ${shadowColors.light.soft}`,
  insetBottom: `inset 0 -2px 4px ${shadowColors.dark.soft}`,
  insetLeft: `inset 2px 0 4px ${shadowColors.light.soft}`,
  insetRight: `inset -2px 0 4px ${shadowColors.dark.soft}`,
} as const;

export type LightShadows = typeof lightShadows;

/**
 * Neomorphic shadow combinations
 * Ready-to-use shadow presets for neomorphic design
 */

import { shadowColors } from '../colors/shadows';

export const neomorphicShadows = {
  // Default neomorphic (raised)
  raised: {
    default: `6px 6px 12px ${shadowColors.dark.medium}, -6px -6px 12px ${shadowColors.light.medium}`,
    hover: `8px 8px 16px ${shadowColors.dark.hard}, -8px -8px 16px ${shadowColors.light.hard}`,
    active: `inset 4px 4px 8px ${shadowColors.dark.medium}, inset -4px -4px 8px ${shadowColors.light.medium}`,
  },
  
  // Pressed neomorphic (inset)
  pressed: {
    default: `inset 4px 4px 8px ${shadowColors.dark.medium}, inset -4px -4px 8px ${shadowColors.light.medium}`,
    hover: `inset 2px 2px 4px ${shadowColors.dark.soft}, inset -2px -2px 4px ${shadowColors.light.soft}`,
  },
  
  // Flat neomorphic (minimal)
  flat: {
    default: `2px 2px 4px ${shadowColors.dark.soft}, -2px -2px 4px ${shadowColors.light.soft}`,
    hover: `4px 4px 8px ${shadowColors.dark.soft}, -4px -4px 8px ${shadowColors.light.soft}`,
  },
  
  // Colored neomorphic (with accent colors)
  colored: {
    primary: `6px 6px 12px ${shadowColors.dark.medium}, -6px -6px 12px ${shadowColors.colored.primary}`,
    success: `6px 6px 12px ${shadowColors.dark.medium}, -6px -6px 12px ${shadowColors.colored.success}`,
    error: `6px 6px 12px ${shadowColors.dark.medium}, -6px -6px 12px ${shadowColors.colored.error}`,
  },
} as const;

export type NeomorphicShadows = typeof neomorphicShadows;

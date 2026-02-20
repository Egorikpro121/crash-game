/**
 * Shadow utilities
 */

import { shadows } from '../tokens/shadows';

export const shadowUtils = {
  // Apply neomorphic shadow
  neomorphic: (variant: 'raised' | 'pressed' | 'flat' = 'raised') => {
    return {
      raised: shadows.neomorphic.raised.default,
      pressed: shadows.neomorphic.pressed.default,
      flat: shadows.neomorphic.flat.default,
    }[variant];
  },
  
  // Apply elevation
  elevation: (level: 0 | 1 | 2 | 3 | 4 | 5) => {
    return shadows.elevations[level];
  },
  
  // Custom shadow
  custom: (x: number, y: number, blur: number, spread: number, color: string) => {
    return `${x}px ${y}px ${blur}px ${spread}px ${color}`;
  },
};

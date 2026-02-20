/**
 * Neomorphic variants
 * Different neomorphic styles for various use cases
 */

import { css } from 'styled-components';
import { shadows } from '../../tokens/shadows';
import { colors } from '../../tokens/colors';

export const neomorphicVariants = {
  // Card variant
  card: css`
    background: ${colors.neutral.surface.light};
    border-radius: 24px;
    box-shadow: ${shadows.neomorphic.raised.default};
    padding: 24px;
  `,
  
  // Button variant
  button: css`
    background: ${colors.neutral.surface.light};
    border-radius: 16px;
    box-shadow: ${shadows.neomorphic.raised.default};
    padding: 12px 24px;
    transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
    
    &:hover {
      box-shadow: ${shadows.neomorphic.raised.hover};
      transform: translateY(-1px);
    }
    
    &:active {
      box-shadow: ${shadows.neomorphic.raised.active};
      transform: translateY(0);
    }
  `,
  
  // Input variant
  input: css`
    background: ${colors.neutral.surface.light};
    border-radius: 16px;
    box-shadow: ${shadows.neomorphic.pressed.default};
    padding: 12px 16px;
    border: none;
    outline: none;
    transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
    
    &:focus {
      box-shadow: ${shadows.neomorphic.flat.default};
    }
  `,
  
  // Elevated variant (for modals, dropdowns)
  elevated: css`
    background: ${colors.neutral.surface.light};
    border-radius: 24px;
    box-shadow: ${shadows.elevations[4]};
  `,
} as const;

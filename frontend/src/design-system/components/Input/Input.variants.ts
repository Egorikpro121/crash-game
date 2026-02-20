/**
 * Input variants
 */

import { css } from 'styled-components';
import { colors } from '../../tokens/colors';
import { shadows } from '../../tokens/shadows';
import { InputVariant } from './Input.types';

export const inputVariants: Record<InputVariant, ReturnType<typeof css>> = {
  default: css`
    background: ${colors.neutral.surface.light};
    border: 1px solid ${colors.neutral.border.medium};
    box-shadow: ${shadows.neomorphic.pressed.default};
    
    &:focus {
      border-color: ${colors.primary.accent.primary};
      box-shadow: ${shadows.neomorphic.flat.default};
    }
  `,
  
  neomorphic: css`
    background: ${colors.neutral.surface.light};
    border: none;
    box-shadow: ${shadows.neomorphic.pressed.default};
    
    &:focus {
      box-shadow: ${shadows.neomorphic.flat.default};
    }
  `,
};

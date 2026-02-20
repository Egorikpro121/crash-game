/**
 * Card variants
 */

import { css } from 'styled-components';
import { shadows } from '../../tokens/shadows';
import { CardVariant } from './Card.types';

export const cardVariants: Record<CardVariant, ReturnType<typeof css>> = {
  default: css`
    box-shadow: ${shadows.neomorphic.raised.default};
  `,
  
  elevated: css`
    box-shadow: ${shadows.elevations[4]};
  `,
  
  flat: css`
    box-shadow: ${shadows.neomorphic.flat.default};
  `,
  
  pressed: css`
    box-shadow: ${shadows.neomorphic.pressed.default};
  `,
};

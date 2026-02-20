/**
 * Base neomorphic styles
 * Core neomorphic design patterns
 */

import { css } from 'styled-components';
import { shadows } from '../../tokens/shadows';
import { colors } from '../../tokens/colors';

export const neomorphicBase = css`
  background: ${colors.neutral.surface.light};
  border-radius: 16px;
  box-shadow: ${shadows.neomorphic.raised.default};
  transition: box-shadow 200ms cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover {
    box-shadow: ${shadows.neomorphic.raised.hover};
  }
  
  &:active {
    box-shadow: ${shadows.neomorphic.raised.active};
  }
`;

export const neomorphicPressed = css`
  background: ${colors.neutral.surface.light};
  border-radius: 16px;
  box-shadow: ${shadows.neomorphic.pressed.default};
  transition: box-shadow 200ms cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover {
    box-shadow: ${shadows.neomorphic.pressed.hover};
  }
`;

export const neomorphicFlat = css`
  background: ${colors.neutral.surface.light};
  border-radius: 16px;
  box-shadow: ${shadows.neomorphic.flat.default};
  transition: box-shadow 200ms cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover {
    box-shadow: ${shadows.neomorphic.flat.hover};
  }
`;

/**
 * Neomorphic mixins
 * Reusable mixins for styled-components
 */

import { css } from 'styled-components';
import { shadows } from '../../tokens/shadows';
import { colors } from '../../tokens/colors';

export const neomorphicMixin = (
  elevation: 'flat' | 'raised' | 'pressed' = 'raised',
  size: 'small' | 'medium' | 'large' = 'medium'
) => {
  const radiusMap = {
    small: '8px',
    medium: '16px',
    large: '24px',
  };
  
  const shadowMap = {
    flat: shadows.neomorphic.flat.default,
    raised: shadows.neomorphic.raised.default,
    pressed: shadows.neomorphic.pressed.default,
  };
  
  return css`
    background: ${colors.neutral.surface.light};
    border-radius: ${radiusMap[size]};
    box-shadow: ${shadowMap[elevation]};
    transition: box-shadow 200ms cubic-bezier(0.4, 0, 0.2, 1);
  `;
};

export const neomorphicHoverMixin = (
  elevation: 'flat' | 'raised' | 'pressed' = 'raised'
) => {
  const shadowMap = {
    flat: shadows.neomorphic.flat.hover,
    raised: shadows.neomorphic.raised.hover,
    pressed: shadows.neomorphic.pressed.hover,
  };
  
  return css`
    &:hover {
      box-shadow: ${shadowMap[elevation]};
      transform: translateY(-1px);
    }
  `;
};

export const neomorphicActiveMixin = () => css`
  &:active {
    box-shadow: ${shadows.neomorphic.raised.active};
    transform: translateY(0);
  }
`;

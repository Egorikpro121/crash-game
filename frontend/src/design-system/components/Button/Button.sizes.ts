/**
 * Button sizes
 */

import { css } from 'styled-components';
import { spacing } from '../../tokens/spacing/scales';
import { typography } from '../../tokens/typography';
import { ButtonSize } from './Button.types';

export const buttonSizes: Record<ButtonSize, ReturnType<typeof css>> = {
  sm: css`
    padding: ${spacing[2]} ${spacing[4]};
    font-size: ${typography.sizes.sm};
    height: 32px;
  `,
  
  md: css`
    padding: ${spacing[3]} ${spacing[6]};
    font-size: ${typography.sizes.base};
    height: 40px;
  `,
  
  lg: css`
    padding: ${spacing[4]} ${spacing[8]};
    font-size: ${typography.sizes.lg};
    height: 48px;
  `,
};

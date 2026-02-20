/**
 * Button styled component
 */

import styled from 'styled-components';
import { ButtonProps } from './Button.types';
import { buttonVariants } from './Button.variants';
import { buttonSizes } from './Button.sizes';
import { radius } from '../../tokens/radius/base';
import { spacing } from '../../tokens/spacing/scales';
import { animation } from '../../tokens/animation';
import { colors } from '../../tokens/colors';

export const StyledButton = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: ${spacing[2]};
  border-radius: ${radius.lg};
  font-weight: 500;
  cursor: pointer;
  transition: all ${animation.durations.normal}ms ${animation.easings.easeInOut};
  border: none;
  outline: none;
  
  ${({ variant = 'primary' }) => buttonVariants[variant]}
  ${({ size = 'md' }) => buttonSizes[size]}
  
  ${({ fullWidth }) => fullWidth && `
    width: 100%;
  `}
  
  ${({ disabled, isLoading }) => (disabled || isLoading) && `
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  `}
  
  &:focus-visible {
    outline: 2px solid ${colors.primary.accent.primary};
    outline-offset: 2px;
  }
`;

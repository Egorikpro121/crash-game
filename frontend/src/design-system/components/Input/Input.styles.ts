/**
 * Input styled component
 */

import styled from 'styled-components';
import { InputProps } from './Input.types';
import { inputVariants } from './Input.variants';
import { spacing } from '../../tokens/spacing/scales';
import { radius } from '../../tokens/radius/base';
import { typography } from '../../tokens/typography';
import { colors } from '../../tokens/colors';
import { animation } from '../../tokens/animation';

const sizeMap = {
  sm: spacing[2],
  md: spacing[3],
  lg: spacing[4],
};

export const StyledInput = styled.input<InputProps>`
  width: 100%;
  padding: ${({ size = 'md' }) => sizeMap[size]} ${spacing[4]};
  border-radius: ${radius.lg};
  font-size: ${typography.sizes.base};
  color: ${colors.neutral.text.primary};
  transition: all ${animation.durations.normal}ms ${animation.easings.easeInOut};
  outline: none;
  
  ${({ variant = 'neomorphic' }) => inputVariants[variant]}
  
  &::placeholder {
    color: ${colors.neutral.text.tertiary};
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  ${({ error }) => error && `
    border-color: ${colors.semantic.error.main};
    box-shadow: 0 0 0 2px ${colors.semantic.error.main}33;
  `}
`;

export const InputWrapper = styled.div<{ fullWidth?: boolean }>`
  display: flex;
  flex-direction: column;
  gap: ${spacing[1]};
  width: ${({ fullWidth }) => fullWidth ? '100%' : 'auto'};
`;

export const InputLabel = styled.label`
  font-size: ${typography.sizes.sm};
  font-weight: ${typography.fonts.weight.medium};
  color: ${colors.neutral.text.secondary};
`;

export const InputError = styled.span`
  font-size: ${typography.sizes.sm};
  color: ${colors.semantic.error.main};
`;

export const InputHelper = styled.span`
  font-size: ${typography.sizes.sm};
  color: ${colors.neutral.text.tertiary};
`;

export const InputContainer = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  
  svg {
    position: absolute;
    left: ${spacing[4]};
    color: ${colors.neutral.text.tertiary};
  }
  
  input {
    padding-left: ${({ hasLeftIcon }: { hasLeftIcon?: boolean }) => 
      hasLeftIcon ? spacing[12] : spacing[4]};
    padding-right: ${({ hasRightIcon }: { hasRightIcon?: boolean }) => 
      hasRightIcon ? spacing[12] : spacing[4]};
  }
`;

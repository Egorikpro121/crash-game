/**
 * Button variants
 */

import { css } from 'styled-components';
import { colors } from '../../tokens/colors';
import { shadows } from '../../tokens/shadows';
import { ButtonVariant } from './Button.types';

export const buttonVariants: Record<ButtonVariant, ReturnType<typeof css>> = {
  primary: css`
    background: ${colors.primary.accent.primary};
    color: ${colors.neutral.text.primary};
    box-shadow: ${shadows.neomorphic.colored.primary};
    
    &:hover {
      background: ${colors.primary.blue[600]};
      box-shadow: ${shadows.neomorphic.raised.hover};
    }
    
    &:active {
      box-shadow: ${shadows.neomorphic.raised.active};
    }
  `,
  
  secondary: css`
    background: ${colors.neutral.surface.light};
    color: ${colors.neutral.text.primary};
    box-shadow: ${shadows.neomorphic.raised.default};
    
    &:hover {
      box-shadow: ${shadows.neomorphic.raised.hover};
    }
    
    &:active {
      box-shadow: ${shadows.neomorphic.raised.active};
    }
  `,
  
  danger: css`
    background: ${colors.semantic.error.main};
    color: ${colors.neutral.text.primary};
    box-shadow: ${shadows.neomorphic.colored.error};
    
    &:hover {
      background: ${colors.semantic.error.dark};
      box-shadow: ${shadows.neomorphic.raised.hover};
    }
    
    &:active {
      box-shadow: ${shadows.neomorphic.raised.active};
    }
  `,
  
  success: css`
    background: ${colors.semantic.success.main};
    color: ${colors.neutral.text.primary};
    box-shadow: ${shadows.neomorphic.colored.success};
    
    &:hover {
      background: ${colors.semantic.success.dark};
      box-shadow: ${shadows.neomorphic.raised.hover};
    }
    
    &:active {
      box-shadow: ${shadows.neomorphic.raised.active};
    }
  `,
  
  ghost: css`
    background: transparent;
    color: ${colors.neutral.text.primary};
    box-shadow: none;
    
    &:hover {
      background: ${colors.neutral.surface.medium};
    }
  `,
};

/**
 * Card styled component
 */

import styled from 'styled-components';
import { CardProps } from './Card.types';
import { cardVariants } from './Card.variants';
import { colors } from '../../tokens/colors';
import { radius } from '../../tokens/radius/base';
import { spacing } from '../../tokens/spacing/scales';
import { animation } from '../../tokens/animation';

const paddingMap = {
  none: '0',
  sm: spacing[4],
  md: spacing[6],
  lg: spacing[8],
};

export const StyledCard = styled.div<CardProps>`
  background: ${colors.neutral.surface.light};
  border-radius: ${radius.xl};
  transition: box-shadow ${animation.durations.normal}ms ${animation.easings.easeInOut};
  
  ${({ variant = 'default' }) => cardVariants[variant]}
  
  ${({ padding = 'md' }) => `
    padding: ${paddingMap[padding]};
  `}
  
  &:hover {
    box-shadow: ${({ variant = 'default' }) => 
      variant === 'default' 
        ? '6px 6px 12px rgba(0, 0, 0, 0.4), -6px -6px 12px rgba(255, 255, 255, 0.08)'
        : 'inherit'};
  }
`;

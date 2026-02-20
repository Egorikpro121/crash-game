import styled from 'styled-components';
import { BadgeProps } from './Badge.types';
import { badgeVariants } from './Badge.variants';
import { radius } from '../../tokens/radius/base';
import { spacing } from '../../tokens/spacing/scales';
import { typography } from '../../tokens/typography';

const sizeMap = {
  sm: {
    padding: `${spacing[1]} ${spacing[2]}`,
    fontSize: typography.sizes.xs,
  },
  md: {
    padding: `${spacing[1.5]} ${spacing[3]}`,
    fontSize: typography.sizes.sm,
  },
  lg: {
    padding: `${spacing[2]} ${spacing[4]}`,
    fontSize: typography.sizes.base,
  },
};

export const StyledBadge = styled.span<BadgeProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: ${radius.full};
  font-weight: ${typography.fonts.weight.medium};
  
  ${({ variant = 'primary' }) => badgeVariants[variant]}
  ${({ size = 'md' }) => `
    padding: ${sizeMap[size].padding};
    font-size: ${sizeMap[size].fontSize};
  `}
`;

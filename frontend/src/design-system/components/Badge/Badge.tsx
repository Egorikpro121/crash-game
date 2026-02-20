import React from 'react';
import { StyledBadge } from './Badge.styles';
import { BadgeProps } from './Badge.types';

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  ...props
}) => {
  return (
    <StyledBadge variant={variant} size={size} {...props}>
      {children}
    </StyledBadge>
  );
};

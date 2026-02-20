/**
 * Card component
 */

import React from 'react';
import { StyledCard } from './Card.styles';
import { CardProps } from './Card.types';

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  padding = 'md',
  ...props
}) => {
  return (
    <StyledCard variant={variant} padding={padding} {...props}>
      {children}
    </StyledCard>
  );
};

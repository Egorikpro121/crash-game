import React from 'react';
import { StyledLoader } from './Loader.styles';
import { LoaderProps } from './Loader.types';

export const Loader: React.FC<LoaderProps> = ({
  variant = 'spinner',
  size = 'md',
  color,
}) => {
  if (variant === 'dots') {
    return (
      <StyledLoader variant={variant} size={size}>
        <span></span>
        <span></span>
        <span></span>
      </StyledLoader>
    );
  }
  
  return <StyledLoader variant={variant} size={size} color={color} />;
};

import styled from 'styled-components';
import { LoaderProps } from './Loader.types';
import { loaderVariants } from './Loader.variants';

const sizeMap = {
  sm: '16px',
  md: '24px',
  lg: '32px',
};

export const StyledLoader = styled.div<LoaderProps>`
  display: inline-block;
  width: ${({ size = 'md' }) => sizeMap[size]};
  height: ${({ size = 'md' }) => sizeMap[size]};
  
  ${({ variant = 'spinner' }) => loaderVariants[variant]}
`;

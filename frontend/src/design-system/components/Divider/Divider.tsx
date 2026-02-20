import React from 'react';
import { StyledDivider } from './Divider.styles';

interface DividerProps {
  vertical?: boolean;
}

export const Divider: React.FC<DividerProps> = ({ vertical = false }) => {
  return <StyledDivider vertical={vertical} />;
};

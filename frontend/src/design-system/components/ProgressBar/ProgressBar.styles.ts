import styled from 'styled-components';
import { colors } from '../../tokens/colors';
import { radius } from '../../tokens/radius/base';
import { shadows } from '../../tokens/shadows';

const sizeMap = {
  sm: '4px',
  md: '8px',
  lg: '12px',
};

export const ProgressBarContainer = styled.div<{ size: string }>`
  width: 100%;
  height: ${({ size }) => sizeMap[size as keyof typeof sizeMap] || sizeMap.md};
  background: ${colors.neutral.surface.medium};
  border-radius: ${radius.full};
  overflow: hidden;
  box-shadow: ${shadows.neomorphic.pressed.default};
`;

export const ProgressBarFill = styled.div<{ value: number; max: number; color?: string }>`
  height: 100%;
  width: ${({ value, max }) => (value / max) * 100}%;
  background: ${({ color }) => color || colors.primary.accent.primary};
  border-radius: ${radius.full};
  transition: width 300ms cubic-bezier(0.4, 0, 0.2, 1);
`;

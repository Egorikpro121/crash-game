import styled from 'styled-components';
import { colors } from '../../../design-system/tokens/colors';
import { gameColors } from '../../../design-system/tokens/colors/game';
import { typography } from '../../../design-system/tokens/typography';
import { shadows } from '../../../design-system/tokens/shadows';
import { multiplierPulse, multiplierGlow } from './MultiplierDisplay.animations';
import { animation } from '../../../design-system/tokens/animation';

const getMultiplierColor = (multiplier: number): string => {
  if (multiplier < 2) return gameColors.multiplier.low;
  if (multiplier < 5) return gameColors.multiplier.medium;
  if (multiplier < 10) return gameColors.multiplier.high;
  return gameColors.multiplier.veryHigh;
};

const sizeMap = {
  sm: typography.sizes['3xl'],
  md: typography.sizes['5xl'],
  lg: typography.sizes['7xl'],
};

export const MultiplierContainer = styled.div<{ multiplier: number; size: string }>`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 10;
`;

export const MultiplierValue = styled.div<{ multiplier: number; size: string }>`
  font-size: ${({ size }) => sizeMap[size as keyof typeof sizeMap] || sizeMap.md};
  font-weight: ${typography.fonts.weight.extrabold};
  color: ${({ multiplier }) => getMultiplierColor(multiplier)};
  text-shadow: ${shadows.neomorphic.flat.default};
  animation: ${multiplierPulse} 2s ${animation.easings.easeInOut} infinite,
             ${multiplierGlow} 2s ${animation.easings.easeInOut} infinite;
  transition: color ${animation.durations.fast}ms ${animation.easings.easeInOut};
`;

export const MultiplierLabel = styled.div`
  font-size: ${typography.sizes.sm};
  color: ${colors.neutral.text.secondary};
  text-transform: uppercase;
  letter-spacing: 2px;
`;

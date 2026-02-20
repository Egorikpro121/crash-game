import styled from 'styled-components';
import { colors } from '../../tokens/colors';
import { shadows } from '../../tokens/shadows';
import { radius } from '../../tokens/radius/base';
import { spacing } from '../../tokens/spacing/scales';
import { zIndex } from '../../tokens/zIndex';
import { typography } from '../../tokens/typography';
import { animation } from '../../tokens/animation';
import { TooltipPosition } from './Tooltip.types';

const positionMap: Record<TooltipPosition, string> = {
  top: `
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-bottom: ${spacing[2]};
  `,
  bottom: `
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: ${spacing[2]};
  `,
  left: `
    right: 100%;
    top: 50%;
    transform: translateY(-50%);
    margin-right: ${spacing[2]};
  `,
  right: `
    left: 100%;
    top: 50%;
    transform: translateY(-50%);
    margin-left: ${spacing[2]};
  `,
};

export const TooltipWrapper = styled.div`
  position: relative;
  display: inline-block;
`;

export const TooltipContent = styled.div<{ position: TooltipPosition; visible: boolean }>`
  position: absolute;
  ${({ position }) => positionMap[position]}
  background: ${colors.neutral.background.elevated};
  color: ${colors.neutral.text.primary};
  padding: ${spacing[2]} ${spacing[3]};
  border-radius: ${radius.base};
  font-size: ${typography.sizes.sm};
  white-space: nowrap;
  z-index: ${zIndex.tooltip};
  box-shadow: ${shadows.elevations[3]};
  opacity: ${({ visible }) => visible ? 1 : 0};
  pointer-events: ${({ visible }) => visible ? 'auto' : 'none'};
  transition: opacity ${animation.durations.fast}ms ${animation.easings.easeOut};
`;

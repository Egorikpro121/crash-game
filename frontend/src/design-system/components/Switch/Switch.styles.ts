import styled from 'styled-components';
import { colors } from '../../tokens/colors';
import { shadows } from '../../tokens/shadows';
import { radius } from '../../tokens/radius/base';
import { spacing } from '../../tokens/spacing/scales';
import { animation } from '../../tokens/animation';

const sizeMap = {
  sm: { width: '32px', height: '18px', thumb: '14px' },
  md: { width: '44px', height: '24px', thumb: '20px' },
  lg: { width: '56px', height: '30px', thumb: '26px' },
};

export const SwitchWrapper = styled.label<{ size: string }>`
  display: inline-flex;
  align-items: center;
  gap: ${spacing[3]};
  cursor: pointer;
`;

export const SwitchInput = styled.input<{ size: string }>`
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  
  &:checked + span {
    background: ${colors.primary.accent.primary};
    
    &::before {
      transform: translateX(${({ size }) => {
        const s = sizeMap[size as keyof typeof sizeMap] || sizeMap.md;
        return `calc(${s.width} - ${s.thumb} - 4px)`;
      }});
    }
  }
  
  &:disabled + span {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

export const SwitchTrack = styled.span<{ size: string }>`
  position: relative;
  display: inline-block;
  width: ${({ size }) => sizeMap[size as keyof typeof sizeMap]?.width || sizeMap.md.width};
  height: ${({ size }) => sizeMap[size as keyof typeof sizeMap]?.height || sizeMap.md.height};
  background: ${colors.neutral.surface.medium};
  border-radius: ${radius.full};
  box-shadow: ${shadows.neomorphic.pressed.default};
  transition: all ${animation.durations.normal}ms ${animation.easings.easeInOut};
  
  &::before {
    content: '';
    position: absolute;
    width: ${({ size }) => sizeMap[size as keyof typeof sizeMap]?.thumb || sizeMap.md.thumb};
    height: ${({ size }) => sizeMap[size as keyof typeof sizeMap]?.thumb || sizeMap.md.thumb};
    left: 2px;
    top: 50%;
    transform: translateY(-50%);
    background: ${colors.neutral.text.primary};
    border-radius: ${radius.full};
    box-shadow: ${shadows.neomorphic.flat.default};
    transition: transform ${animation.durations.normal}ms ${animation.easings.easeInOut};
  }
`;

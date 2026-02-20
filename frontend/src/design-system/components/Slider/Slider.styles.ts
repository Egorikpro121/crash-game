import styled from 'styled-components';
import { colors } from '../../tokens/colors';
import { radius } from '../../tokens/radius/base';
import { shadows } from '../../tokens/shadows';
import { spacing } from '../../tokens/spacing/scales';
import { animation } from '../../tokens/animation';

export const SliderWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[2]};
  width: 100%;
`;

export const SliderInput = styled.input`
  width: 100%;
  height: 8px;
  border-radius: ${radius.full};
  background: ${colors.neutral.surface.medium};
  outline: none;
  box-shadow: ${shadows.neomorphic.pressed.default};
  -webkit-appearance: none;
  
  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: ${radius.full};
    background: ${colors.primary.accent.primary};
    cursor: pointer;
    box-shadow: ${shadows.neomorphic.raised.default};
    transition: all ${animation.durations.fast}ms;
    
    &:hover {
      box-shadow: ${shadows.neomorphic.raised.hover};
      transform: scale(1.1);
    }
  }
  
  &::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: ${radius.full};
    background: ${colors.primary.accent.primary};
    cursor: pointer;
    border: none;
    box-shadow: ${shadows.neomorphic.raised.default};
  }
`;

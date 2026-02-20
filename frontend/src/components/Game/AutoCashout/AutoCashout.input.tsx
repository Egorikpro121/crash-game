import React from 'react';
import { Input } from '../../../design-system/components/Input';
import { Slider } from '../../../design-system/components/Slider';
import styled from 'styled-components';
import { spacing } from '../../../design-system/tokens/spacing/scales';

const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[3]};
`;

interface AutoCashoutInputProps {
  multiplier: number;
  onMultiplierChange: (multiplier: number) => void;
  min?: number;
  max?: number;
}

export const AutoCashoutInput: React.FC<AutoCashoutInputProps> = ({
  multiplier,
  onMultiplierChange,
  min = 1.01,
  max = 100,
}) => {
  return (
    <InputContainer>
      <Input
        type="number"
        value={multiplier}
        onChange={(e) => onMultiplierChange(parseFloat(e.target.value) || min)}
        min={min}
        max={max}
        step={0.01}
      />
      <Slider
        value={multiplier}
        onChange={(e) => onMultiplierChange(parseFloat(e.target.value))}
        min={min}
        max={max}
        step={0.01}
        showValue
      />
    </InputContainer>
  );
};

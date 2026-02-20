import React from 'react';
import { SliderWrapper, SliderInput } from './Slider.styles';
import { SliderProps } from './Slider.types';

export const Slider: React.FC<SliderProps> = ({
  label,
  showValue = false,
  min = 0,
  max = 100,
  step = 1,
  value,
  ...props
}) => {
  return (
    <SliderWrapper>
      {label && (
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>{label}</span>
          {showValue && <span>{value}</span>}
        </div>
      )}
      <SliderInput
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        {...props}
      />
    </SliderWrapper>
  );
};

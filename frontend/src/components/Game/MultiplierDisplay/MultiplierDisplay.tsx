import React from 'react';
import {
  MultiplierContainer,
  MultiplierValue,
  MultiplierLabel,
} from './MultiplierDisplay.styles';
import { MultiplierDisplayProps } from './MultiplierDisplay.types';

export const MultiplierDisplay: React.FC<MultiplierDisplayProps> = ({
  multiplier,
  size = 'lg',
}) => {
  return (
    <MultiplierContainer multiplier={multiplier} size={size}>
      <MultiplierValue multiplier={multiplier} size={size}>
        {multiplier.toFixed(2)}x
      </MultiplierValue>
      <MultiplierLabel>Multiplier</MultiplierLabel>
    </MultiplierContainer>
  );
};

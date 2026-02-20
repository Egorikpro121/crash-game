import React from 'react';
import { SwitchWrapper, SwitchInput, SwitchTrack } from './Switch.styles';
import { SwitchProps } from './Switch.types';

export const Switch: React.FC<SwitchProps> = ({
  label,
  size = 'md',
  ...props
}) => {
  return (
    <SwitchWrapper size={size}>
      <SwitchInput type="checkbox" size={size} {...props} />
      <SwitchTrack size={size} />
      {label && <span>{label}</span>}
    </SwitchWrapper>
  );
};

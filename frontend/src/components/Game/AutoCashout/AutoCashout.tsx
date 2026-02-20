import React from 'react';
import {
  AutoCashoutContainer,
  AutoCashoutHeader,
} from './AutoCashout.styles';
import { AutoCashoutProps } from './AutoCashout.types';
import { Switch } from '../../../design-system/components/Switch';
import { AutoCashoutInput } from './AutoCashout.input';

export const AutoCashout: React.FC<AutoCashoutProps> = ({
  enabled,
  multiplier = 2.0,
  onToggle,
  onMultiplierChange,
}) => {
  return (
    <AutoCashoutContainer>
      <AutoCashoutHeader>
        <span>Auto Cashout</span>
        <Switch checked={enabled} onChange={(e) => onToggle(e.target.checked)} />
      </AutoCashoutHeader>
      {enabled && (
        <AutoCashoutInput
          multiplier={multiplier}
          onMultiplierChange={onMultiplierChange}
        />
      )}
    </AutoCashoutContainer>
  );
};

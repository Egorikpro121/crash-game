import React from 'react';
import { Button } from '../../../design-system/components/Button';
import styled from 'styled-components';
import { spacing } from '../../../design-system/tokens/spacing/scales';

const CurrencySelector = styled.div`
  display: flex;
  gap: ${spacing[2]};
`;

interface CurrencySelectorProps {
  currency: string;
  onCurrencyChange: (currency: string) => void;
}

export const CurrencySelectorComponent: React.FC<CurrencySelectorProps> = ({
  currency,
  onCurrencyChange,
}) => {
  return (
    <CurrencySelector>
      <Button
        variant={currency === 'TON' ? 'primary' : 'secondary'}
        onClick={() => onCurrencyChange('TON')}
      >
        TON
      </Button>
      <Button
        variant={currency === 'STARS' ? 'primary' : 'secondary'}
        onClick={() => onCurrencyChange('STARS')}
      >
        STARS
      </Button>
    </CurrencySelector>
  );
};

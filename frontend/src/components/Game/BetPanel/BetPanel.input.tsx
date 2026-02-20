import React, { useState } from 'react';
import { Input } from '../../../design-system/components/Input';
import { Button } from '../../../design-system/components/Button';
import { spacing } from '../../../design-system/tokens/spacing/scales';
import styled from 'styled-components';

const QuickAmounts = styled.div`
  display: flex;
  gap: ${spacing[2]};
  flex-wrap: wrap;
`;

const quickAmounts = [0.1, 0.5, 1, 5, 10];

interface BetInputProps {
  currency: string;
  onAmountChange: (amount: number) => void;
}

export const BetInput: React.FC<BetInputProps> = ({ currency, onAmountChange }) => {
  const [amount, setAmount] = useState('');
  
  const handleQuickAmount = (value: number) => {
    setAmount(value.toString());
    onAmountChange(value);
  };
  
  return (
    <div>
      <Input
        type="number"
        placeholder={`Amount in ${currency}`}
        value={amount}
        onChange={(e) => {
          setAmount(e.target.value);
          onAmountChange(parseFloat(e.target.value) || 0);
        }}
      />
      <QuickAmounts>
        {quickAmounts.map((value) => (
          <Button
            key={value}
            size="sm"
            variant="secondary"
            onClick={() => handleQuickAmount(value)}
          >
            {value} {currency}
          </Button>
        ))}
      </QuickAmounts>
    </div>
  );
};

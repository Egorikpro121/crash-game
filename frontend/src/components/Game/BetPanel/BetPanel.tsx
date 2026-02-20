import React, { useState } from 'react';
import { BetPanelContainer } from './BetPanel.styles';
import { BetPanelProps } from './BetPanel.types';
import { BetInput } from './BetPanel.input';
import { CurrencySelectorComponent } from './BetPanel.currency';
import { BetActions } from './BetPanel.actions';

export const BetPanel: React.FC<BetPanelProps> = ({
  onBet,
  onCashout,
  hasActiveBet = false,
  canBet = true,
}) => {
  const [currency, setCurrency] = useState('TON');
  const [amount, setAmount] = useState(0);
  
  const handleBet = () => {
    if (amount > 0 && onBet) {
      onBet(amount, currency);
    }
  };
  
  return (
    <BetPanelContainer>
      <CurrencySelectorComponent
        currency={currency}
        onCurrencyChange={setCurrency}
      />
      {!hasActiveBet && (
        <BetInput currency={currency} onAmountChange={setAmount} />
      )}
      <BetActions
        hasActiveBet={hasActiveBet}
        canBet={canBet}
        onBet={handleBet}
        onCashout={onCashout || (() => {})}
      />
    </BetPanelContainer>
  );
};

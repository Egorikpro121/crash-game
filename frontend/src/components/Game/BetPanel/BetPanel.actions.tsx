import React from 'react';
import { Button } from '../../../design-system/components/Button';
import styled from 'styled-components';
import { spacing } from '../../../design-system/tokens/spacing/scales';

const ActionsContainer = styled.div`
  display: flex;
  gap: ${spacing[4]};
  width: 100%;
`;

interface BetActionsProps {
  hasActiveBet: boolean;
  canBet: boolean;
  onBet: () => void;
  onCashout: () => void;
}

export const BetActions: React.FC<BetActionsProps> = ({
  hasActiveBet,
  canBet,
  onBet,
  onCashout,
}) => {
  if (hasActiveBet) {
    return (
      <ActionsContainer>
        <Button variant="success" fullWidth onClick={onCashout}>
          Cash Out
        </Button>
      </ActionsContainer>
    );
  }
  
  return (
    <ActionsContainer>
      <Button
        variant="primary"
        fullWidth
        onClick={onBet}
        disabled={!canBet}
      >
        Place Bet
      </Button>
    </ActionsContainer>
  );
};

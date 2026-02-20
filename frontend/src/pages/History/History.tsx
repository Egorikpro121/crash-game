import React from 'react';
import styled from 'styled-components';
import { colors } from '../../design-system/tokens/colors';
import { spacing } from '../../design-system/tokens/spacing/scales';
import { HistoryPanel } from '../../components/Game/HistoryPanel';

const HistoryContainer = styled.div`
  padding: ${spacing[4]};
  min-height: 100vh;
  background: ${colors.neutral.background.base};
`;

export const History: React.FC = () => {
  const mockHistory = [
    { roundId: 1, multiplier: 2.5, crashedAt: new Date() },
    { roundId: 2, multiplier: 1.8, crashedAt: new Date() },
  ];
  
  return (
    <HistoryContainer>
      <h1>Game History</h1>
      <HistoryPanel history={mockHistory} />
    </HistoryContainer>
  );
};

import React from 'react';
import styled from 'styled-components';
import { colors } from '../../design-system/tokens/colors';
import { spacing } from '../../design-system/tokens/spacing/scales';
import { ProvablyFair as ProvablyFairComponent } from '../../components/Game/ProvablyFair';

const ProvablyFairContainer = styled.div`
  padding: ${spacing[4]};
  min-height: 100vh;
  background: ${colors.neutral.background.base};
`;

export const ProvablyFairPage: React.FC = () => {
  return (
    <ProvablyFairContainer>
      <h1>Provably Fair</h1>
      <ProvablyFairComponent
        roundId={1}
        serverSeedHash="hash123"
        crashMultiplier={2.5}
      />
    </ProvablyFairContainer>
  );
};

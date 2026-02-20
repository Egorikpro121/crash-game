import React from 'react';
import styled from 'styled-components';
import { colors } from '../../design-system/tokens/colors';
import { spacing } from '../../design-system/tokens/spacing/scales';
import { Card } from '../../design-system/components/Card';

const LeaderboardContainer = styled.div`
  padding: ${spacing[4]};
  min-height: 100vh;
  background: ${colors.neutral.background.base};
`;

export const Leaderboard: React.FC = () => {
  return (
    <LeaderboardContainer>
      <h1>Leaderboard</h1>
      <Card>
        <p>Leaderboard content will be here</p>
      </Card>
    </LeaderboardContainer>
  );
};

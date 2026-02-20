import React from 'react';
import styled from 'styled-components';
import { colors } from '../../design-system/tokens/colors';
import { spacing } from '../../design-system/tokens/spacing/scales';
import { Card } from '../../design-system/components/Card';

const SupportContainer = styled.div`
  padding: ${spacing[4]};
  min-height: 100vh;
  background: ${colors.neutral.background.base};
`;

export const Support: React.FC = () => {
  return (
    <SupportContainer>
      <h1>Support</h1>
      <Card>
        <p>Contact support here</p>
      </Card>
    </SupportContainer>
  );
};

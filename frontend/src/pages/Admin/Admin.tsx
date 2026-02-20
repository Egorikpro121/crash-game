import React from 'react';
import styled from 'styled-components';
import { colors } from '../../design-system/tokens/colors';
import { spacing } from '../../design-system/tokens/spacing/scales';
import { Card } from '../../design-system/components/Card';

const AdminContainer = styled.div`
  padding: ${spacing[4]};
  min-height: 100vh;
  background: ${colors.neutral.background.base};
`;

export const Admin: React.FC = () => {
  return (
    <AdminContainer>
      <h1>Admin Panel</h1>
      <Card>
        <p>Admin content will be here</p>
      </Card>
    </AdminContainer>
  );
};

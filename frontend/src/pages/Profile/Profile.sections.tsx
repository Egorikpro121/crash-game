import React from 'react';
import { Card } from '../../design-system/components/Card';
import styled from 'styled-components';
import { spacing } from '../../design-system/tokens/spacing/scales';

const Section = styled(Card)`
  display: flex;
  flex-direction: column;
  gap: ${spacing[4]};
`;

export const ProfileStats: React.FC = () => (
  <Section>
    <h3>Statistics</h3>
    {/* Stats content */}
  </Section>
);

export const ProfileSettings: React.FC = () => (
  <Section>
    <h3>Settings</h3>
    {/* Settings content */}
  </Section>
);

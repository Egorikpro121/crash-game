import React from 'react';
import styled from 'styled-components';
import { spacing } from '../../design-system/tokens/spacing/scales';

const GameLayoutContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: ${spacing[4]};
  padding: ${spacing[4]};
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const MainArea = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[4]};
`;

const Sidebar = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[4]};
`;

interface GameLayoutProps {
  main: React.ReactNode;
  sidebar: React.ReactNode;
}

export const GameLayout: React.FC<GameLayoutProps> = ({ main, sidebar }) => {
  return (
    <GameLayoutContainer>
      <MainArea>{main}</MainArea>
      <Sidebar>{sidebar}</Sidebar>
    </GameLayoutContainer>
  );
};

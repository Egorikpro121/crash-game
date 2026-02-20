import React from 'react';
import { HomeContainer, HomeHeader, HomeContent } from './Home.styles';
import { HomeProps } from './Home.types';
import { Button } from '../../design-system/components/Button';
import { Card } from '../../design-system/components/Card';
import { useNavigate } from 'react-router-dom';

export const Home: React.FC<HomeProps> = () => {
  const navigate = useNavigate();
  
  return (
    <HomeContainer>
      <HomeHeader>
        <h1>Crash Game</h1>
        <p>Place your bets and cash out before the crash!</p>
      </HomeHeader>
      
      <HomeContent>
        <Card>
          <Button fullWidth onClick={() => navigate('/game')}>
            Start Playing
          </Button>
        </Card>
        
        <Card>
          <h3>How to Play</h3>
          <p>1. Place your bet</p>
          <p>2. Watch the multiplier grow</p>
          <p>3. Cash out before it crashes!</p>
        </Card>
      </HomeContent>
    </HomeContainer>
  );
};

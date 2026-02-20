/**
 * CrashGame main component
 */

import React from 'react';
import { GameContainer, GameCanvasWrapper, GameControls } from './CrashGame.styles';
import { CrashGameProps } from './CrashGame.types';
import { useGameState } from './CrashGame.hooks';
import { GameCanvas } from '../GameCanvas';
import { MultiplierDisplay } from '../MultiplierDisplay';
import { BetPanel } from '../BetPanel';

export const CrashGame: React.FC<CrashGameProps> = ({
  onBet,
  onCashout,
  currentMultiplier,
  roundStatus = 'pending',
}) => {
  const { multiplier, isActive, hasBet } = useGameState();
  
  const displayMultiplier = currentMultiplier || multiplier;
  
  return (
    <GameContainer>
      <GameCanvasWrapper>
        <GameCanvas multiplier={displayMultiplier} isActive={isActive} />
        <MultiplierDisplay multiplier={displayMultiplier} />
      </GameCanvasWrapper>
      
      <GameControls>
        <BetPanel
          onBet={onBet}
          onCashout={onCashout}
          hasActiveBet={hasBet}
          canBet={roundStatus !== 'crashed'}
        />
      </GameControls>
    </GameContainer>
  );
};

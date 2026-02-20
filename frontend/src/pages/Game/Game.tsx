import React from 'react';
import { GamePageContainer } from './Game.styles';
import { GameProps } from './Game.types';
import { GameLayout } from './Game.layout';
import { CrashGame } from '../../components/Game/CrashGame';
import { HistoryPanel } from '../../components/Game/HistoryPanel';
import { PlayersList } from '../../components/Game/PlayersList';

export const Game: React.FC<GameProps> = () => {
  // Mock data - in production would come from API/WebSocket
  const mockHistory = [
    { roundId: 1, multiplier: 2.5, crashedAt: new Date() },
    { roundId: 2, multiplier: 1.8, crashedAt: new Date() },
  ];
  
  const mockPlayers = [
    { id: 1, username: 'Player1', bet: 1.0, multiplier: 2.0, cashedOut: true },
    { id: 2, username: 'Player2', bet: 0.5, cashedOut: false },
  ];
  
  return (
    <GamePageContainer>
      <GameLayout
        main={<CrashGame />}
        sidebar={
          <>
            <HistoryPanel history={mockHistory} />
            <PlayersList players={mockPlayers} />
          </>
        }
      />
    </GamePageContainer>
  );
};

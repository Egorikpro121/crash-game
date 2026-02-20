import React from 'react';
import {
  PlayersListContainer,
  PlayersTitle,
} from './PlayersList.styles';
import { PlayersListProps } from './PlayersList.types';
import { PlayerItem } from './PlayersList.item';

export const PlayersList: React.FC<PlayersListProps> = ({
  players,
  currentUserId,
}) => {
  return (
    <PlayersListContainer>
      <PlayersTitle>Active Players</PlayersTitle>
      {players.map((player) => (
        <PlayerItem
          key={player.id}
          {...player}
          isCurrentUser={player.id === currentUserId}
        />
      ))}
    </PlayersListContainer>
  );
};

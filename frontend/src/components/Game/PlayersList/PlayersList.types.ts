export interface Player {
  id: number;
  username: string;
  bet: number;
  multiplier?: number;
  cashedOut: boolean;
}

export interface PlayersListProps {
  players: Player[];
  currentUserId?: number;
}

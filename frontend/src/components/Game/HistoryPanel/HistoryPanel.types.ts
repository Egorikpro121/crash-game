export interface HistoryItem {
  roundId: number;
  multiplier: number;
  crashedAt: Date;
}

export interface HistoryPanelProps {
  history: HistoryItem[];
  limit?: number;
}

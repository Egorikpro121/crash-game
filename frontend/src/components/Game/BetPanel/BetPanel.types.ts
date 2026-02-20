export interface BetPanelProps {
  onBet?: (amount: number, currency: string) => void;
  onCashout?: () => void;
  hasActiveBet?: boolean;
  canBet?: boolean;
}

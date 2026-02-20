/**
 * CrashGame component types
 */

export interface CrashGameProps {
  onBet?: (amount: number, currency: string) => void;
  onCashout?: () => void;
  currentMultiplier?: number;
  roundStatus?: 'pending' | 'active' | 'crashed';
}

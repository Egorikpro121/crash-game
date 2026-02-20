export interface AutoCashoutProps {
  enabled: boolean;
  multiplier?: number;
  onToggle: (enabled: boolean) => void;
  onMultiplierChange: (multiplier: number) => void;
}

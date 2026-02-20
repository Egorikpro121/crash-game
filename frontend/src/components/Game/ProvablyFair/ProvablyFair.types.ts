export interface ProvablyFairProps {
  roundId: number;
  serverSeedHash: string;
  serverSeed?: string;
  clientSeed?: string;
  crashMultiplier?: number;
}

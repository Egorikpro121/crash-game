/**
 * Game-specific tokens export
 */

export * from './multipliers';
export * from './crash';
export * from './bets';

import { multiplierTokens } from './multipliers';
import { crashTokens } from './crash';
import { betTokens } from './bets';

export const gameTokens = {
  multipliers: multiplierTokens,
  crash: crashTokens,
  bets: betTokens,
} as const;

export type GameTokens = typeof gameTokens;

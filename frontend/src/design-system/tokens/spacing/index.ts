/**
 * Spacing tokens export
 */

export * from './base';
export * from './scales';

import { spacingBase } from './base';
import { spacing } from './scales';

export const spacingTokens = {
  base: spacingBase,
  scale: spacing,
} as const;

export type SpacingTokens = typeof spacingTokens;

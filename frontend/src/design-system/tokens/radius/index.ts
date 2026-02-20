/**
 * Radius tokens export
 */

export * from './base';
export * from './components';

import { radius } from './base';
import { componentRadius } from './components';

export const radiusTokens = {
  base: radius,
  components: componentRadius,
} as const;

export type RadiusTokens = typeof radiusTokens;

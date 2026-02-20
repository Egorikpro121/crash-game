/**
 * Z-index tokens export
 */

export * from './layers';

import { zIndex } from './layers';

export const zIndexTokens = zIndex;

export type ZIndexTokens = typeof zIndexTokens;

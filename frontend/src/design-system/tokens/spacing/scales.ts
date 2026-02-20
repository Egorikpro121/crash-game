/**
 * Spacing scale
 * Based on 4px base unit
 */

import { spacingBase } from './base';

export const spacing = {
  0: '0',
  0.5: `${spacingBase * 0.5}px`,  // 2px
  1: `${spacingBase * 1}px`,       // 4px
  1.5: `${spacingBase * 1.5}px`,   // 6px
  2: `${spacingBase * 2}px`,       // 8px
  2.5: `${spacingBase * 2.5}px`,   // 10px
  3: `${spacingBase * 3}px`,       // 12px
  3.5: `${spacingBase * 3.5}px`,   // 14px
  4: `${spacingBase * 4}px`,        // 16px
  5: `${spacingBase * 5}px`,        // 20px
  6: `${spacingBase * 6}px`,        // 24px
  7: `${spacingBase * 7}px`,        // 28px
  8: `${spacingBase * 8}px`,        // 32px
  9: `${spacingBase * 9}px`,        // 36px
  10: `${spacingBase * 10}px`,      // 40px
  11: `${spacingBase * 11}px`,      // 44px
  12: `${spacingBase * 12}px`,      // 48px
  14: `${spacingBase * 14}px`,      // 56px
  16: `${spacingBase * 16}px`,      // 64px
  20: `${spacingBase * 20}px`,      // 80px
  24: `${spacingBase * 24}px`,      // 96px
  28: `${spacingBase * 28}px`,      // 112px
  32: `${spacingBase * 32}px`,      // 128px
  36: `${spacingBase * 36}px`,      // 144px
  40: `${spacingBase * 40}px`,      // 160px
  44: `${spacingBase * 44}px`,      // 176px
  48: `${spacingBase * 48}px`,      // 192px
  52: `${spacingBase * 52}px`,      // 208px
  56: `${spacingBase * 56}px`,      // 224px
  60: `${spacingBase * 60}px`,      // 240px
  64: `${spacingBase * 64}px`,      // 256px
} as const;

export type Spacing = typeof spacing;

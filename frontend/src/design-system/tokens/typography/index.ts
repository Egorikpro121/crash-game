/**
 * Typography tokens export
 */

export * from './fonts';
export * from './sizes';
export * from './lineHeights';
export * from './letterSpacing';
export * from './styles';

import { fonts } from './fonts';
import { fontSizes } from './sizes';
import { lineHeights } from './lineHeights';
import { letterSpacing } from './letterSpacing';
import { typographyStyles } from './styles';

export const typography = {
  fonts,
  sizes: fontSizes,
  lineHeights,
  letterSpacing,
  styles: typographyStyles,
} as const;

export type Typography = typeof typography;

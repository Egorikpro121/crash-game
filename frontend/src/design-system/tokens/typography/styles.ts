/**
 * Typography styles
 * Pre-defined text styles for headings and body text
 */

import { fonts } from './fonts';
import { fontSizes } from './sizes';
import { lineHeights } from './lineHeights';
import { letterSpacing } from './letterSpacing';

export const typographyStyles = {
  // Headings
  h1: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes['5xl'],
    fontWeight: fonts.weight.bold,
    lineHeight: lineHeights.tight,
    letterSpacing: letterSpacing.tight,
  },
  
  h2: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes['4xl'],
    fontWeight: fonts.weight.bold,
    lineHeight: lineHeights.tight,
    letterSpacing: letterSpacing.tight,
  },
  
  h3: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes['3xl'],
    fontWeight: fonts.weight.semibold,
    lineHeight: lineHeights.snug,
    letterSpacing: letterSpacing.normal,
  },
  
  h4: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes['2xl'],
    fontWeight: fonts.weight.semibold,
    lineHeight: lineHeights.snug,
    letterSpacing: letterSpacing.normal,
  },
  
  h5: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes.xl,
    fontWeight: fonts.weight.semibold,
    lineHeight: lineHeights.normal,
    letterSpacing: letterSpacing.normal,
  },
  
  h6: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes.lg,
    fontWeight: fonts.weight.semibold,
    lineHeight: lineHeights.normal,
    letterSpacing: letterSpacing.normal,
  },
  
  // Body text
  body: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes.base,
    fontWeight: fonts.weight.regular,
    lineHeight: lineHeights.relaxed,
    letterSpacing: letterSpacing.normal,
  },
  
  bodyLarge: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes.lg,
    fontWeight: fonts.weight.regular,
    lineHeight: lineHeights.relaxed,
    letterSpacing: letterSpacing.normal,
  },
  
  bodySmall: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes.sm,
    fontWeight: fonts.weight.regular,
    lineHeight: lineHeights.normal,
    letterSpacing: letterSpacing.normal,
  },
  
  // Special text
  caption: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes.sm,
    fontWeight: fonts.weight.regular,
    lineHeight: lineHeights.normal,
    letterSpacing: letterSpacing.wide,
  },
  
  label: {
    fontFamily: fonts.family.primary,
    fontSize: fontSizes.sm,
    fontWeight: fonts.weight.medium,
    lineHeight: lineHeights.normal,
    letterSpacing: letterSpacing.wide,
  },
  
  // Display text (for large numbers, multipliers)
  display: {
    fontFamily: fonts.family.display,
    fontSize: fontSizes['7xl'],
    fontWeight: fonts.weight.extrabold,
    lineHeight: lineHeights.none,
    letterSpacing: letterSpacing.tighter,
  },
  
  // Monospace (for addresses, hashes)
  mono: {
    fontFamily: fonts.family.mono,
    fontSize: fontSizes.base,
    fontWeight: fonts.weight.regular,
    lineHeight: lineHeights.relaxed,
    letterSpacing: letterSpacing.normal,
  },
} as const;

export type TypographyStyles = typeof typographyStyles;

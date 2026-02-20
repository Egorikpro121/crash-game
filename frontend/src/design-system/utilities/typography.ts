/**
 * Typography utilities
 */

import { typography } from '../tokens/typography';

export const typographyUtils = {
  // Apply typography style
  applyStyle: (styleName: keyof typeof typography.styles) => {
    return typography.styles[styleName];
  },
  
  // Get font size
  fontSize: (size: keyof typeof typography.sizes) => {
    return { fontSize: typography.sizes[size] };
  },
  
  // Get font weight
  fontWeight: (weight: keyof typeof typography.fonts.weight) => {
    return { fontWeight: typography.fonts.weight[weight] };
  },
  
  // Get line height
  lineHeight: (height: keyof typeof typography.lineHeights) => {
    return { lineHeight: typography.lineHeights[height] };
  },
  
  // Truncate text
  truncate: {
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap' as const,
  },
  
  // Line clamp
  lineClamp: (lines: number) => ({
    display: '-webkit-box',
    WebkitLineClamp: lines,
    WebkitBoxOrient: 'vertical' as const,
    overflow: 'hidden',
  }),
};

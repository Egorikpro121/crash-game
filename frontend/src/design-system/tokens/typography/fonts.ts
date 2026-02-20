/**
 * Font families and weights
 */

export const fonts = {
  // Font families
  family: {
    primary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    mono: "'JetBrains Mono', 'Fira Code', 'Courier New', monospace",
    display: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
  },
  
  // Font weights
  weight: {
    light: 300,
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
  },
} as const;

export type Fonts = typeof fonts;

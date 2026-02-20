/**
 * Primary colors for Neomorphism Dark Theme
 * Telegram-inspired color palette
 */

export const primaryColors = {
  // Telegram Blue
  blue: {
    50: '#e3f2fd',
    100: '#bbdefb',
    200: '#90caf9',
    300: '#64b5f6',
    400: '#42a5f5',
    500: '#0088cc', // Main Telegram blue
    600: '#0077b6',
    700: '#0066a0',
    800: '#00558a',
    900: '#003d63',
  },
  
  // Accent colors
  accent: {
    primary: '#0088cc',
    secondary: '#00d4aa',
    tertiary: '#ff6b6b',
  },
  
  // Brand colors
  brand: {
    telegram: '#0088cc',
    ton: '#0088cc',
    stars: '#ffd700',
  },
} as const;

export type PrimaryColors = typeof primaryColors;

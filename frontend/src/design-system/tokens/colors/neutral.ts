/**
 * Neutral colors for Neomorphism Dark Theme
 * Gray scale optimized for dark backgrounds
 */

export const neutralColors = {
  // Background colors (dark theme)
  background: {
    base: '#1a1a1a',      // Main background
    elevated: '#2d2d2d',   // Elevated surfaces
    pressed: '#1f1f1f',   // Pressed state
    hover: '#252525',     // Hover state
  },
  
  // Surface colors (for neomorphic elements)
  surface: {
    light: '#2d2d2d',     // Light surface
    medium: '#252525',    // Medium surface
    dark: '#1f1f1f',      // Dark surface
  },
  
  // Text colors
  text: {
    primary: '#ffffff',   // Primary text
    secondary: '#b3b3b3', // Secondary text
    tertiary: '#808080',  // Tertiary text
    disabled: '#4d4d4d',  // Disabled text
    inverse: '#1a1a1a',  // Inverse text (on light)
  },
  
  // Border colors
  border: {
    light: '#3d3d3d',
    medium: '#2d2d2d',
    dark: '#1d1d1d',
  },
  
  // Gray scale
  gray: {
    50: '#f5f5f5',
    100: '#e0e0e0',
    200: '#bdbdbd',
    300: '#9e9e9e',
    400: '#757575',
    500: '#616161',
    600: '#424242',
    700: '#303030',
    800: '#212121',
    900: '#1a1a1a',
  },
} as const;

export type NeutralColors = typeof neutralColors;

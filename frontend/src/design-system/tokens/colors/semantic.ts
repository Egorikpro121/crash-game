/**
 * Semantic colors for UI states
 * Success, error, warning, info
 */

export const semanticColors = {
  success: {
    light: '#4caf50',
    main: '#00d4aa',
    dark: '#00b894',
    contrast: '#ffffff',
  },
  
  error: {
    light: '#ef5350',
    main: '#ff3333',
    dark: '#c62828',
    contrast: '#ffffff',
  },
  
  warning: {
    light: '#ffb74d',
    main: '#ff9800',
    dark: '#f57c00',
    contrast: '#1a1a1a',
  },
  
  info: {
    light: '#42a5f5',
    main: '#0088cc',
    dark: '#0066a0',
    contrast: '#ffffff',
  },
} as const;

export type SemanticColors = typeof semanticColors;

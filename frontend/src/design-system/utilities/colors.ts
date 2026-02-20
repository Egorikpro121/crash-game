/**
 * Color utilities
 */

import { colors } from '../tokens/colors';

export const colorUtils = {
  // Get color by path (e.g., 'primary.accent.primary')
  get: (path: string): string => {
    const parts = path.split('.');
    let value: any = colors;
    for (const part of parts) {
      value = value[part];
      if (!value) return '';
    }
    return typeof value === 'string' ? value : '';
  },
  
  // Opacity helpers
  withOpacity: (color: string, opacity: number): string => {
    if (color.startsWith('#')) {
      const r = parseInt(color.slice(1, 3), 16);
      const g = parseInt(color.slice(3, 5), 16);
      const b = parseInt(color.slice(5, 7), 16);
      return `rgba(${r}, ${g}, ${b}, ${opacity})`;
    }
    return color;
  },
  
  // Lighten color
  lighten: (color: string, percent: number): string => {
    // Simplified - in production would use color manipulation library
    return color;
  },
  
  // Darken color
  darken: (color: string, percent: number): string => {
    // Simplified - in production would use color manipulation library
    return color;
  },
};

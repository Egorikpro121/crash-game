/**
 * useTheme hook
 * Hook to access theme in components
 */

import { useThemeContext } from './ThemeProvider';
import { Theme } from './types';

export const useTheme = (): Theme => {
  const { theme } = useThemeContext();
  return theme;
};

/**
 * Theme Provider
 * Provides theme context to the application
 */

import React, { createContext, useContext, ReactNode } from 'react';
import { Theme, ThemeContextValue } from './types';
import { tokens } from '../../tokens';

const defaultTheme: Theme = {
  ...tokens,
  mode: 'dark',
};

const ThemeContext = createContext<ThemeContextValue>({
  theme: defaultTheme,
});

interface ThemeProviderProps {
  children: ReactNode;
  theme?: Theme;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({
  children,
  theme = defaultTheme,
}) => {
  return (
    <ThemeContext.Provider value={{ theme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useThemeContext = () => {
  return useContext(ThemeContext);
};

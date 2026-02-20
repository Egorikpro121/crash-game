/**
 * Theme types
 */

import { Tokens } from '../../tokens';

export interface Theme extends Tokens {
  mode: 'dark';
}

export interface ThemeContextValue {
  theme: Theme;
  setTheme?: (theme: Theme) => void;
}

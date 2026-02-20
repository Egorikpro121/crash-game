/**
 * Responsive mixins
 */

import { css } from 'styled-components';
import { breakpointTokens } from '../../tokens/breakpoints';

export const responsive = {
  mobile: (styles: string) => css`
    @media (max-width: ${parseInt(breakpointTokens.sizes.md) - 1}px) {
      ${styles}
    }
  `,
  
  tablet: (styles: string) => css`
    @media (min-width: ${breakpointTokens.sizes.md}) and (max-width: ${parseInt(breakpointTokens.sizes.lg) - 1}px) {
      ${styles}
    }
  `,
  
  desktop: (styles: string) => css`
    @media (min-width: ${breakpointTokens.sizes.lg}) {
      ${styles}
    }
  `,
  
  // Breakpoint-specific
  sm: (styles: string) => css`
    @media (min-width: ${breakpointTokens.sizes.sm}) {
      ${styles}
    }
  `,
  
  md: (styles: string) => css`
    @media (min-width: ${breakpointTokens.sizes.md}) {
      ${styles}
    }
  `,
  
  lg: (styles: string) => css`
    @media (min-width: ${breakpointTokens.sizes.lg}) {
      ${styles}
    }
  `,
  
  xl: (styles: string) => css`
    @media (min-width: ${breakpointTokens.sizes.xl}) {
      ${styles}
    }
  `,
};

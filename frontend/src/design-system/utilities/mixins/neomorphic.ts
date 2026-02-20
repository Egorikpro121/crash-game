/**
 * Neomorphic mixins
 */

import { css } from 'styled-components';
import { neomorphicMixin, neomorphicHoverMixin, neomorphicActiveMixin } from '../../foundations/neomorphic/mixins';

export const neomorphic = {
  raised: (size: 'small' | 'medium' | 'large' = 'medium') => css`
    ${neomorphicMixin('raised', size)}
    ${neomorphicHoverMixin('raised')}
    ${neomorphicActiveMixin()}
  `,
  
  pressed: (size: 'small' | 'medium' | 'large' = 'medium') => css`
    ${neomorphicMixin('pressed', size)}
    ${neomorphicHoverMixin('pressed')}
  `,
  
  flat: (size: 'small' | 'medium' | 'large' = 'medium') => css`
    ${neomorphicMixin('flat', size)}
    ${neomorphicHoverMixin('flat')}
  `,
};

/**
 * Common transitions
 */

import { css } from 'styled-components';
import { animation } from '../../tokens/animation';

export const transitionBase = css`
  transition: all ${animation.durations.normal}ms ${animation.easings.easeInOut};
`;

export const transitionFast = css`
  transition: all ${animation.durations.fast}ms ${animation.easings.easeInOut};
`;

export const transitionSlow = css`
  transition: all ${animation.durations.slow}ms ${animation.easings.easeInOut};
`;

export const transitionColors = css`
  transition: color ${animation.durations.fast}ms ${animation.easings.easeInOut},
              background-color ${animation.durations.fast}ms ${animation.easings.easeInOut},
              border-color ${animation.durations.fast}ms ${animation.easings.easeInOut};
`;

export const transitionTransform = css`
  transition: transform ${animation.durations.normal}ms ${animation.easings.easeOut};
`;

export const transitionOpacity = css`
  transition: opacity ${animation.durations.fast}ms ${animation.easings.easeInOut};
`;

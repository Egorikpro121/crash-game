/**
 * Component-specific transitions
 */

import { css } from 'styled-components';
import { animation } from '../../tokens/animation';

export const buttonTransition = css`
  transition: all ${animation.durations.normal}ms ${animation.easings.easeInOut};
  
  &:hover {
    transition: all ${animation.durations.fast}ms ${animation.easings.easeOut};
  }
  
  &:active {
    transition: all ${animation.durations.fast}ms ${animation.easings.easeIn};
  }
`;

export const modalTransition = css`
  transition: opacity ${animation.durations.normal}ms ${animation.easings.easeOut},
              transform ${animation.durations.normal}ms ${animation.easings.easeOut};
`;

export const tooltipTransition = css`
  transition: opacity ${animation.durations.fast}ms ${animation.easings.easeOut},
              transform ${animation.durations.fast}ms ${animation.easings.easeOut};
`;

export const cardTransition = css`
  transition: box-shadow ${animation.durations.normal}ms ${animation.easings.easeInOut},
              transform ${animation.durations.normal}ms ${animation.easings.easeInOut};
  
  &:hover {
    transition: box-shadow ${animation.durations.fast}ms ${animation.easings.easeOut},
                transform ${animation.durations.fast}ms ${animation.easings.easeOut};
  }
`;

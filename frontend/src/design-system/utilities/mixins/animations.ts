/**
 * Animation mixins
 */

import { css } from 'styled-components';
import { animation } from '../../tokens/animation';
import * as keyframes from '../../animations/keyframes';

export const animationMixins = {
  fadeIn: css`
    animation: ${keyframes.fadeIn} ${animation.durations.normal}ms ${animation.easings.easeOut};
  `,
  
  fadeOut: css`
    animation: ${keyframes.fadeOut} ${animation.durations.normal}ms ${animation.easings.easeIn};
  `,
  
  slideUp: css`
    animation: ${keyframes.slideUp} ${animation.durations.normal}ms ${animation.easings.easeOut};
  `,
  
  slideDown: css`
    animation: ${keyframes.slideDown} ${animation.durations.normal}ms ${animation.easings.easeOut};
  `,
  
  scaleIn: css`
    animation: ${keyframes.scaleIn} ${animation.durations.normal}ms ${animation.easings.easeOut};
  `,
  
  pulse: css`
    animation: ${keyframes.pulse} 2s ${animation.easings.easeInOut} infinite;
  `,
  
  rotate: css`
    animation: ${keyframes.rotate} 1s linear infinite;
  `,
};

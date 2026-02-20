/**
 * Pulse animations
 */

import { keyframes } from 'styled-components';

export const pulse = keyframes`
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
`;

export const pulseGlow = keyframes`
  0%, 100% {
    box-shadow: 0 0 5px rgba(0, 136, 204, 0.5);
  }
  50% {
    box-shadow: 0 0 20px rgba(0, 136, 204, 0.8);
  }
`;

export const pulseScale = keyframes`
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
`;

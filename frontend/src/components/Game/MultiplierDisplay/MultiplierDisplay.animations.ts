import { keyframes } from 'styled-components';
import { gameColors } from '../../../design-system/tokens/colors/game';

export const multiplierPulse = keyframes`
  0%, 100% {
    transform: scale(1);
    filter: brightness(1);
  }
  50% {
    transform: scale(1.05);
    filter: brightness(1.2);
  }
`;

export const multiplierGlow = keyframes`
  0%, 100% {
    text-shadow: 0 0 10px ${gameColors.multiplier.low};
  }
  50% {
    text-shadow: 0 0 20px ${gameColors.multiplier.high}, 0 0 30px ${gameColors.multiplier.high};
  }
`;

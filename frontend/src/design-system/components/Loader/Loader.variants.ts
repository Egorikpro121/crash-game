import { css, keyframes } from 'styled-components';
import { colors } from '../../tokens/colors';

const spin = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

const dots = keyframes`
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
`;

export const loaderVariants = {
  spinner: css`
    border: 3px solid ${colors.neutral.surface.medium};
    border-top-color: ${colors.primary.accent.primary};
    border-radius: 50%;
    animation: ${spin} 1s linear infinite;
  `,
  
  pulse: css`
    background: ${colors.primary.accent.primary};
    border-radius: 50%;
    animation: ${pulse} 1.5s ease-in-out infinite;
  `,
  
  dots: css`
    span {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: ${colors.primary.accent.primary};
      animation: ${dots} 1.4s infinite ease-in-out both;
      
      &:nth-child(1) { animation-delay: -0.32s; }
      &:nth-child(2) { animation-delay: -0.16s; }
    }
  `,
};

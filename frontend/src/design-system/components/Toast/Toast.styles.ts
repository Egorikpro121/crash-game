import styled, { keyframes } from 'styled-components';
import { ToastProps } from './Toast.types';
import { colors } from '../../tokens/colors';
import { shadows } from '../../tokens/shadows';
import { radius } from '../../tokens/radius/base';
import { spacing } from '../../tokens/spacing/scales';
import { zIndex } from '../../tokens/zIndex';
import { animation } from '../../tokens/animation';

const slideIn = keyframes`
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
`;

const slideOut = keyframes`
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
`;

const variantColors = {
  success: colors.semantic.success.main,
  error: colors.semantic.error.main,
  warning: colors.semantic.warning.main,
  info: colors.semantic.info.main,
};

export const ToastContainer = styled.div`
  position: fixed;
  top: ${spacing[4]};
  right: ${spacing[4]};
  z-index: ${zIndex.toast};
  display: flex;
  flex-direction: column;
  gap: ${spacing[2]};
`;

export const StyledToast = styled.div<ToastProps>`
  background: ${colors.neutral.surface.light};
  border-left: 4px solid ${({ variant = 'info' }) => variantColors[variant]};
  border-radius: ${radius.lg};
  box-shadow: ${shadows.elevations[3]};
  padding: ${spacing[4]} ${spacing[6]};
  min-width: 300px;
  max-width: 400px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: ${spacing[4]};
  animation: ${slideIn} ${animation.durations.normal}ms ${animation.easings.easeOut};
  
  &.closing {
    animation: ${slideOut} ${animation.durations.normal}ms ${animation.easings.easeIn};
  }
`;

export const ToastCloseButton = styled.button`
  background: none;
  border: none;
  color: ${colors.neutral.text.secondary};
  cursor: pointer;
  padding: ${spacing[1]};
  border-radius: ${radius.base};
  
  &:hover {
    background: ${colors.neutral.surface.medium};
    color: ${colors.neutral.text.primary};
  }
`;

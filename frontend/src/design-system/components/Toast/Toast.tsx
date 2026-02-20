import React from 'react';
import { StyledToast, ToastCloseButton } from './Toast.styles';
import { ToastProps } from './Toast.types';

export const Toast: React.FC<ToastProps> = ({ message, variant = 'info', onClose }) => {
  return (
    <StyledToast variant={variant}>
      <span>{message}</span>
      <ToastCloseButton onClick={onClose}>×</ToastCloseButton>
    </StyledToast>
  );
};

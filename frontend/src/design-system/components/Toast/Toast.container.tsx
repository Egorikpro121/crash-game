import React, { useState, useEffect } from 'react';
import { ToastContainer, StyledToast, ToastCloseButton } from './Toast.styles';
import { Toast } from './Toast.types';

interface ToastContainerProps {
  toasts: Toast[];
  onRemove: (id: string) => void;
}

export const ToastList: React.FC<ToastContainerProps> = ({ toasts, onRemove }) => {
  return (
    <ToastContainer>
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onClose={() => onRemove(toast.id)} />
      ))}
    </ToastContainer>
  );
};

interface ToastItemProps {
  toast: Toast;
  onClose: () => void;
}

const ToastItem: React.FC<ToastItemProps> = ({ toast, onClose }) => {
  const [isClosing, setIsClosing] = useState(false);
  
  useEffect(() => {
    if (toast.duration) {
      const timer = setTimeout(() => {
        setIsClosing(true);
        setTimeout(onClose, 200);
      }, toast.duration);
      
      return () => clearTimeout(timer);
    }
  }, [toast.duration, onClose]);
  
  return (
    <StyledToast variant={toast.variant} className={isClosing ? 'closing' : ''}>
      <span>{toast.message}</span>
      <ToastCloseButton onClick={onClose}>×</ToastCloseButton>
    </StyledToast>
  );
};

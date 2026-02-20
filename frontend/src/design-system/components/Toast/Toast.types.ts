import { ReactNode } from 'react';

export type ToastVariant = 'success' | 'error' | 'warning' | 'info';

export interface ToastData {
  id: string;
  message: ReactNode;
  variant?: ToastVariant;
  duration?: number;
}

export interface ToastProps extends ToastData {
  onClose: () => void;
}

import { useState, useCallback } from 'react';
import { Toast } from './Toast.types';

export const useToast = () => {
  const [toasts, setToasts] = useState<Toast[]>([]);
  
  const showToast = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    setToasts((prev) => [...prev, { ...toast, id }]);
  }, []);
  
  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);
  
  return { toasts, showToast, removeToast };
};

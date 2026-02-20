/**
 * useAnimation hook
 * Hook for controlling animations
 */

import { useState, useEffect, useRef } from 'react';

export interface UseAnimationOptions {
  duration?: number;
  delay?: number;
  onComplete?: () => void;
}

export const useAnimation = (
  isActive: boolean,
  options: UseAnimationOptions = {}
) => {
  const { duration = 300, delay = 0, onComplete } = options;
  const [isAnimating, setIsAnimating] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  
  useEffect(() => {
    if (isActive) {
      if (delay > 0) {
        timeoutRef.current = setTimeout(() => {
          setIsAnimating(true);
        }, delay);
      } else {
        setIsAnimating(true);
      }
    } else {
      setIsAnimating(false);
    }
    
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [isActive, delay]);
  
  useEffect(() => {
    if (isAnimating && duration > 0) {
      const timer = setTimeout(() => {
        setIsAnimating(false);
        onComplete?.();
      }, duration);
      
      return () => clearTimeout(timer);
    }
  }, [isAnimating, duration, onComplete]);
  
  return isAnimating;
};

/**
 * useTransition hook
 * Hook for transition animations
 */

import { useState, useEffect } from 'react';
import { animation } from '../../tokens/animation';

export interface UseTransitionOptions {
  duration?: number;
  delay?: number;
  easing?: string;
}

export const useTransition = <T>(
  value: T,
  options: UseTransitionOptions = {}
) => {
  const { duration = animation.durations.normal, delay = 0, easing = animation.easings.easeInOut } = options;
  const [displayValue, setDisplayValue] = useState(value);
  const [isTransitioning, setIsTransitioning] = useState(false);
  
  useEffect(() => {
    setIsTransitioning(true);
    
    const timer = setTimeout(() => {
      setDisplayValue(value);
      setIsTransitioning(false);
    }, delay);
    
    return () => clearTimeout(timer);
  }, [value, delay]);
  
  return { displayValue, isTransitioning, duration, easing };
};

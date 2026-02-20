/**
 * useSpring hook
 * Hook for spring animations
 */

import { useState, useEffect } from 'react';
import { animation } from '../../tokens/animation';

export interface UseSpringOptions {
  stiffness?: number;
  damping?: number;
  mass?: number;
}

export const useSpring = (
  target: number,
  options: UseSpringOptions = {}
) => {
  const { stiffness = 100, damping = 10, mass = 1 } = options;
  const [value, setValue] = useState(target);
  const [velocity, setVelocity] = useState(0);
  
  useEffect(() => {
    const spring = () => {
      const force = (target - value) * stiffness;
      const dampingForce = velocity * damping;
      const acceleration = (force - dampingForce) / mass;
      
      setVelocity((v) => v + acceleration * 0.016); // ~60fps
      setValue((v) => v + velocity * 0.016);
    };
    
    const interval = setInterval(spring, 16);
    
    return () => clearInterval(interval);
  }, [target, value, velocity, stiffness, damping, mass]);
  
  return value;
};

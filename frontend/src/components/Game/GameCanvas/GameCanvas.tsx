import React, { useRef, useEffect } from 'react';
import { CanvasContainer } from './GameCanvas.styles';
import { GameCanvasProps } from './GameCanvas.types';
import { CanvasDrawer } from './GameCanvas.draw';
import { colors } from '../../../design-system/tokens/colors';

export const GameCanvas: React.FC<GameCanvasProps> = ({
  multiplier,
  isActive,
  width = 800,
  height = 400,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const drawerRef = useRef<CanvasDrawer | null>(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    canvas.width = width;
    canvas.height = height;
    
    if (!drawerRef.current) {
      drawerRef.current = new CanvasDrawer(ctx);
    }
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Draw grid
    ctx.strokeStyle = colors.neutral.border.medium;
    ctx.lineWidth = 1;
    for (let i = 0; i <= 10; i++) {
      const y = (height / 10) * i;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
    
    // Draw line
    if (isActive && multiplier > 1) {
      drawerRef.current.addPoint(multiplier, width, height);
      
      ctx.strokeStyle = colors.primary.accent.primary;
      ctx.lineWidth = 3;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      drawerRef.current.draw();
    }
  }, [multiplier, isActive, width, height]);
  
  return <CanvasContainer ref={canvasRef} />;
};

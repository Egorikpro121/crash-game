import React from 'react';
import { ProgressBarContainer, ProgressBarFill } from './ProgressBar.styles';
import { ProgressBarProps } from './ProgressBar.types';

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  showLabel = false,
  color,
  size = 'md',
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  
  return (
    <div>
      {showLabel && <span>{percentage.toFixed(0)}%</span>}
      <ProgressBarContainer size={size}>
        <ProgressBarFill value={value} max={max} color={color} />
      </ProgressBarContainer>
    </div>
  );
};

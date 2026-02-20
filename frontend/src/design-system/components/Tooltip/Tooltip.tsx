import React, { useState } from 'react';
import { TooltipWrapper, TooltipContent } from './Tooltip.styles';
import { TooltipProps } from './Tooltip.types';

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  children,
  position = 'top',
  delay = 200,
}) => {
  const [visible, setVisible] = useState(false);
  const [timeoutId, setTimeoutId] = useState<ReturnType<typeof setTimeout> | null>(null);
  
  const handleMouseEnter = () => {
    const id = setTimeout(() => setVisible(true), delay);
    setTimeoutId(id);
  };
  
  const handleMouseLeave = () => {
    if (timeoutId) clearTimeout(timeoutId);
    setVisible(false);
  };
  
  return (
    <TooltipWrapper
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {children}
      <TooltipContent position={position} visible={visible}>
        {content}
      </TooltipContent>
    </TooltipWrapper>
  );
};

/**
 * Icon component
 */

import React from 'react';
import { IconProps } from './types';
import { icons } from './icons';

export const Icon: React.FC<IconProps> = ({
  name,
  size = 24,
  color = 'currentColor',
  ...props
}) => {
  const IconComponent = icons[name];
  
  if (!IconComponent) {
    console.warn(`Icon "${name}" not found`);
    return null;
  }
  
  return (
    <IconComponent
      width={size}
      height={size}
      fill={color}
      {...props}
    />
  );
};

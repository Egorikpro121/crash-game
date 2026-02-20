import React from 'react';
import { StyledAvatar } from './Avatar.styles';
import { AvatarProps } from './Avatar.types';

const getInitials = (name?: string): string => {
  if (!name) return '?';
  const parts = name.trim().split(' ');
  if (parts.length === 1) return parts[0][0].toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};

export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  size = 'md',
  name,
  ...props
}) => {
  return (
    <StyledAvatar size={size} {...props}>
      {src ? (
        <img src={src} alt={alt || name} />
      ) : (
        <span>{getInitials(name)}</span>
      )}
    </StyledAvatar>
  );
};

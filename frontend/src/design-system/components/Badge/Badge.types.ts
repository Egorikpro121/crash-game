import { HTMLAttributes, ReactNode } from 'react';

export type BadgeVariant = 'primary' | 'success' | 'error' | 'warning' | 'neutral';
export type BadgeSize = 'sm' | 'md' | 'lg';

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  size?: BadgeSize;
  children: ReactNode;
}

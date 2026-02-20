/**
 * Card component types
 */

import { HTMLAttributes, ReactNode } from 'react';

export type CardVariant = 'default' | 'elevated' | 'flat' | 'pressed';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  children: ReactNode;
}

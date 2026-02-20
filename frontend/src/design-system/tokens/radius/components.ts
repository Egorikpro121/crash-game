/**
 * Component-specific border radius
 */

import { radius } from './base';

export const componentRadius = {
  button: radius.lg,
  input: radius.lg,
  card: radius.xl,
  modal: radius['2xl'],
  badge: radius.full,
  avatar: radius.full,
  switch: radius.full,
  slider: radius.full,
} as const;

export type ComponentRadius = typeof componentRadius;

/**
 * Icon types
 */

import { SVGProps } from 'react';

export type IconName =
  | 'home'
  | 'game'
  | 'profile'
  | 'deposit'
  | 'withdraw'
  | 'history'
  | 'leaderboard'
  | 'settings'
  | 'close'
  | 'check'
  | 'arrow-left'
  | 'arrow-right'
  | 'arrow-up'
  | 'arrow-down'
  | 'plus'
  | 'minus'
  | 'cashout'
  | 'bet'
  | 'crash'
  | 'multiplier'
  | 'ton'
  | 'stars'
  | 'info'
  | 'warning'
  | 'error'
  | 'success';

export interface IconProps extends SVGProps<SVGSVGElement> {
  name: IconName;
  size?: number | string;
  color?: string;
}

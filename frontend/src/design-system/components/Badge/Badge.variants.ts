import { css } from 'styled-components';
import { colors } from '../../tokens/colors';
import { BadgeVariant } from './Badge.types';

export const badgeVariants: Record<BadgeVariant, ReturnType<typeof css>> = {
  primary: css`
    background: ${colors.primary.accent.primary};
    color: ${colors.neutral.text.primary};
  `,
  success: css`
    background: ${colors.semantic.success.main};
    color: ${colors.neutral.text.primary};
  `,
  error: css`
    background: ${colors.semantic.error.main};
    color: ${colors.neutral.text.primary};
  `,
  warning: css`
    background: ${colors.semantic.warning.main};
    color: ${colors.neutral.text.primary};
  `,
  neutral: css`
    background: ${colors.neutral.surface.medium};
    color: ${colors.neutral.text.secondary};
  `,
};

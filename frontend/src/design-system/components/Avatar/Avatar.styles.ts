import styled from 'styled-components';
import { AvatarProps } from './Avatar.types';
import { avatarSizes } from './Avatar.sizes';
import { colors } from '../../tokens/colors';
import { shadows } from '../../tokens/shadows';
import { radius } from '../../tokens/radius/base';
import { typography } from '../../tokens/typography';

export const StyledAvatar = styled.div<AvatarProps>`
  width: ${({ size = 'md' }) => avatarSizes[size]};
  height: ${({ size = 'md' }) => avatarSizes[size]};
  border-radius: ${radius.full};
  background: ${colors.neutral.surface.medium};
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: ${shadows.neomorphic.flat.default};
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  span {
    font-size: ${({ size = 'md' }) => 
      size === 'xs' ? typography.sizes.xs :
      size === 'sm' ? typography.sizes.sm :
      size === 'lg' ? typography.sizes.lg :
      typography.sizes.base};
    font-weight: ${typography.fonts.weight.semibold};
    color: ${colors.neutral.text.primary};
  }
`;

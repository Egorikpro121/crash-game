import styled from 'styled-components';
import { colors } from '../../../design-system/tokens/colors';
import { shadows } from '../../../design-system/tokens/shadows';
import { radius } from '../../../design-system/tokens/radius/base';
import { spacing } from '../../../design-system/tokens/spacing/scales';

export const ProvablyFairContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[4]};
  padding: ${spacing[6]};
  background: ${colors.neutral.surface.light};
  border-radius: ${radius.xl};
  box-shadow: ${shadows.neomorphic.raised.default};
`;

/**
 * CrashGame styles
 */

import styled from 'styled-components';
import { colors } from '../../../design-system/tokens/colors';
import { shadows } from '../../../design-system/tokens/shadows';
import { radius } from '../../../design-system/tokens/radius/base';
import { spacing } from '../../../design-system/tokens/spacing/scales';

export const GameContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[6]};
  width: 100%;
  height: 100%;
  padding: ${spacing[4]};
  background: ${colors.neutral.background.base};
`;

export const GameCanvasWrapper = styled.div`
  position: relative;
  width: 100%;
  height: 400px;
  border-radius: ${radius.xl};
  background: ${colors.neutral.surface.light};
  box-shadow: ${shadows.neomorphic.raised.default};
  overflow: hidden;
`;

export const GameControls = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[4]};
`;

import styled from 'styled-components';
import { colors } from '../../../design-system/tokens/colors';
import { shadows } from '../../../design-system/tokens/shadows';
import { radius } from '../../../design-system/tokens/radius/base';
import { spacing } from '../../../design-system/tokens/spacing/scales';

export const HistoryPanelContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[2]};
  padding: ${spacing[4]};
  background: ${colors.neutral.surface.light};
  border-radius: ${radius.xl};
  box-shadow: ${shadows.neomorphic.raised.default};
  max-height: 300px;
  overflow-y: auto;
`;

export const HistoryTitle = styled.h3`
  margin-bottom: ${spacing[4]};
`;

import styled from 'styled-components';
import { colors } from '../../../design-system/tokens/colors';
import { radius } from '../../../design-system/tokens/radius/base';

export const CanvasContainer = styled.canvas`
  width: 100%;
  height: 100%;
  background: ${colors.neutral.background.base};
  border-radius: ${radius.xl};
`;

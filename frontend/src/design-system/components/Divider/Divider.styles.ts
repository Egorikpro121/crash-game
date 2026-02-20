import styled from 'styled-components';
import { colors } from '../../tokens/colors';
import { spacing } from '../../tokens/spacing/scales';

export const StyledDivider = styled.hr<{ vertical?: boolean }>`
  border: none;
  background: ${colors.neutral.border.medium};
  ${({ vertical }) => vertical 
    ? `width: 1px; height: 100%; margin: 0 ${spacing[4]};`
    : `height: 1px; width: 100%; margin: ${spacing[4]} 0;`}
`;

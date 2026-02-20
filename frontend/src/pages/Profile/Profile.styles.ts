import styled from 'styled-components';
import { colors } from '../../design-system/tokens/colors';
import { spacing } from '../../design-system/tokens/spacing/scales';

export const ProfileContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[6]};
  padding: ${spacing[4]};
  min-height: 100vh;
  background: ${colors.neutral.background.base};
`;

export const ProfileHeader = styled.div`
  display: flex;
  align-items: center;
  gap: ${spacing[4]};
`;

export const ProfileSections = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[6]};
`;

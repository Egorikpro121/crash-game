import React from 'react';
import styled from 'styled-components';
import { Avatar } from '../../../design-system/components/Avatar';
import { colors } from '../../../design-system/tokens/colors';
import { spacing } from '../../../design-system/tokens/spacing/scales';
import { radius } from '../../../design-system/tokens/radius/base';
import { typography } from '../../../design-system/tokens/typography';
import { Player } from './PlayersList.types';

const PlayerItemContainer = styled.div<{ isCurrentUser: boolean }>`
  display: flex;
  align-items: center;
  gap: ${spacing[3]};
  padding: ${spacing[3]};
  background: ${({ isCurrentUser }) =>
    isCurrentUser ? colors.neutral.surface.medium : 'transparent'};
  border-radius: ${radius.lg};
`;

const PlayerInfo = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: ${spacing[1]};
`;

const PlayerName = styled.span`
  font-size: ${typography.sizes.base};
  font-weight: ${typography.fonts.weight.medium};
  color: ${colors.neutral.text.primary};
`;

const PlayerBet = styled.span`
  font-size: ${typography.sizes.sm};
  color: ${colors.neutral.text.secondary};
`;

const MultiplierBadge = styled.span`
  font-size: ${typography.sizes.sm};
  font-weight: ${typography.fonts.weight.bold};
  color: ${colors.semantic.success.main};
`;

export const PlayerItem: React.FC<Player & { isCurrentUser: boolean }> = ({
  username,
  bet,
  multiplier,
  cashedOut,
  isCurrentUser,
}) => {
  return (
    <PlayerItemContainer isCurrentUser={isCurrentUser}>
      <Avatar name={username} size="sm" />
      <PlayerInfo>
        <PlayerName>{username}</PlayerName>
        <PlayerBet>Bet: {bet}</PlayerBet>
      </PlayerInfo>
      {cashedOut && multiplier && (
        <MultiplierBadge>{multiplier.toFixed(2)}x</MultiplierBadge>
      )}
    </PlayerItemContainer>
  );
};

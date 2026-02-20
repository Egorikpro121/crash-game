import React from 'react';
import styled from 'styled-components';
import { colors } from '../../../design-system/tokens/colors';
import { gameColors } from '../../../design-system/tokens/colors/game';
import { spacing } from '../../../design-system/tokens/spacing/scales';
import { radius } from '../../../design-system/tokens/radius/base';
import { typography } from '../../../design-system/tokens/typography';
import { HistoryItem } from './HistoryPanel.types';

const getMultiplierColor = (multiplier: number): string => {
  if (multiplier < 2) return gameColors.multiplier.low;
  if (multiplier < 5) return gameColors.multiplier.medium;
  if (multiplier < 10) return gameColors.multiplier.high;
  return gameColors.multiplier.veryHigh;
};

const HistoryItemContainer = styled.div<{ multiplier: number }>`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${spacing[3]} ${spacing[4]};
  background: ${colors.neutral.surface.medium};
  border-radius: ${radius.lg};
  border-left: 4px solid ${({ multiplier }) => getMultiplierColor(multiplier)};
`;

const MultiplierText = styled.span<{ multiplier: number }>`
  font-size: ${typography.sizes.lg};
  font-weight: ${typography.fonts.weight.bold};
  color: ${({ multiplier }) => getMultiplierColor(multiplier)};
`;

const RoundIdText = styled.span`
  font-size: ${typography.sizes.sm};
  color: ${colors.neutral.text.secondary};
`;

export const HistoryItemComponent: React.FC<HistoryItem> = ({
  roundId,
  multiplier,
  crashedAt,
}) => {
  return (
    <HistoryItemContainer multiplier={multiplier}>
      <RoundIdText>#{roundId}</RoundIdText>
      <MultiplierText multiplier={multiplier}>
        {multiplier.toFixed(2)}x
      </MultiplierText>
    </HistoryItemContainer>
  );
};

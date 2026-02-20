import React from 'react';
import {
  HistoryPanelContainer,
  HistoryTitle,
} from './HistoryPanel.styles';
import { HistoryPanelProps } from './HistoryPanel.types';
import { HistoryItemComponent } from './HistoryPanel.item';

export const HistoryPanel: React.FC<HistoryPanelProps> = ({
  history,
  limit = 10,
}) => {
  const displayHistory = history.slice(0, limit);
  
  return (
    <HistoryPanelContainer>
      <HistoryTitle>Recent Games</HistoryTitle>
      {displayHistory.map((item) => (
        <HistoryItemComponent key={item.roundId} {...item} />
      ))}
    </HistoryPanelContainer>
  );
};

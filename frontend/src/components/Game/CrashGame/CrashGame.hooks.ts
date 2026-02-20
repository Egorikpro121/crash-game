/**
 * CrashGame hooks
 */

import { useState, useEffect } from 'react';

export const useGameState = () => {
  const [multiplier, setMultiplier] = useState(1.0);
  const [isActive, setIsActive] = useState(false);
  const [hasBet, setHasBet] = useState(false);
  
  return {
    multiplier,
    setMultiplier,
    isActive,
    setIsActive,
    hasBet,
    setHasBet,
  };
};

export const useWebSocketConnection = (url: string) => {
  const [connected, setConnected] = useState(false);
  const [data, setData] = useState<any>(null);
  
  useEffect(() => {
    // WebSocket connection logic
    // Placeholder
    setConnected(true);
  }, [url]);
  
  return { connected, data };
};

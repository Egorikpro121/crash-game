import React from 'react';
import { ProvablyFairContainer } from './ProvablyFair.styles';
import { ProvablyFairProps } from './ProvablyFair.types';
import { VerifyComponent } from './ProvablyFair.verify';

export const ProvablyFair: React.FC<ProvablyFairProps> = ({
  roundId,
  serverSeedHash,
  serverSeed,
  clientSeed,
  crashMultiplier = 0,
}) => {
  if (!serverSeed) {
    return (
      <ProvablyFairContainer>
        <p>Server seed will be revealed after the round ends.</p>
        <p>Server Seed Hash: {serverSeedHash}</p>
      </ProvablyFairContainer>
    );
  }
  
  return (
    <ProvablyFairContainer>
      <VerifyComponent
        serverSeedHash={serverSeedHash}
        serverSeed={serverSeed}
        clientSeed={clientSeed || ''}
        roundId={roundId}
        crashMultiplier={crashMultiplier}
      />
    </ProvablyFairContainer>
  );
};

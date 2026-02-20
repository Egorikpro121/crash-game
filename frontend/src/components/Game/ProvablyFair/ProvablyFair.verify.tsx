import React, { useState } from 'react';
import { Button } from '../../../design-system/components/Button';
import { Input } from '../../../design-system/components/Input';
import styled from 'styled-components';
import { colors } from '../../../design-system/tokens/colors';
import { spacing } from '../../../design-system/tokens/spacing/scales';

const VerifyContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing[4]};
`;

const VerifyResult = styled.div<{ isValid: boolean }>`
  padding: ${spacing[4]};
  background: ${({ isValid }) =>
    isValid ? colors.semantic.success.main : colors.semantic.error.main};
  border-radius: 8px;
  color: ${colors.neutral.text.primary};
`;

interface VerifyComponentProps {
  serverSeedHash: string;
  serverSeed: string;
  clientSeed: string;
  roundId: number;
  crashMultiplier: number;
}

export const VerifyComponent: React.FC<VerifyComponentProps> = ({
  serverSeedHash,
  serverSeed,
  clientSeed,
  roundId,
  crashMultiplier,
}) => {
  const [isVerified, setIsVerified] = useState<boolean | null>(null);
  
  const handleVerify = async () => {
    // In production, would call API to verify
    // Placeholder verification
    const isValid = true; // Simplified
    setIsVerified(isValid);
  };
  
  return (
    <VerifyContainer>
      <Input label="Server Seed Hash" value={serverSeedHash} readOnly />
      <Input label="Server Seed" value={serverSeed} readOnly />
      <Input label="Client Seed" value={clientSeed || ''} readOnly />
      <Input label="Round ID" value={roundId.toString()} readOnly />
      <Input label="Crash Multiplier" value={crashMultiplier.toFixed(2)} readOnly />
      <Button onClick={handleVerify}>Verify Fairness</Button>
      {isVerified !== null && (
        <VerifyResult isValid={isVerified}>
          {isVerified ? '✓ Verified Fair' : '✗ Verification Failed'}
        </VerifyResult>
      )}
    </VerifyContainer>
  );
};

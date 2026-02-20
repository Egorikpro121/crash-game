import React from 'react';
import { DepositContainer } from './Deposit.styles';
import { Card } from '../../design-system/components/Card';
import { Input } from '../../design-system/components/Input';
import { Button } from '../../design-system/components/Button';

export const Deposit: React.FC = () => {
  return (
    <DepositContainer>
      <h1>Deposit</h1>
      <Card>
        <Input label="Amount" type="number" />
        <Button fullWidth>Deposit</Button>
      </Card>
    </DepositContainer>
  );
};

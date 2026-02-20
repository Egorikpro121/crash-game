import React from 'react';
import { WithdrawContainer } from './Withdraw.styles';
import { Card } from '../../design-system/components/Card';
import { Input } from '../../design-system/components/Input';
import { Button } from '../../design-system/components/Button';

export const Withdraw: React.FC = () => {
  return (
    <WithdrawContainer>
      <h1>Withdraw</h1>
      <Card>
        <Input label="Amount" type="number" />
        <Input label="Address" />
        <Button fullWidth>Withdraw</Button>
      </Card>
    </WithdrawContainer>
  );
};

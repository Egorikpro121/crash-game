/**
 * Input component
 */

import React from 'react';
import {
  StyledInput,
  InputWrapper,
  InputLabel,
  InputError,
  InputHelper,
  InputContainer,
} from './Input.styles';
import { InputProps } from './Input.types';

export const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  leftIcon,
  rightIcon,
  fullWidth = false,
  ...props
}) => {
  return (
    <InputWrapper fullWidth={fullWidth}>
      {label && <InputLabel>{label}</InputLabel>}
      <InputContainer hasLeftIcon={!!leftIcon} hasRightIcon={!!rightIcon}>
        {leftIcon && <span>{leftIcon}</span>}
        <StyledInput error={error} {...props} />
        {rightIcon && <span>{rightIcon}</span>}
      </InputContainer>
      {error && <InputError>{error}</InputError>}
      {helperText && !error && <InputHelper>{helperText}</InputHelper>}
    </InputWrapper>
  );
};

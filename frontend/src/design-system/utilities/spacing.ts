/**
 * Spacing utilities
 */

import { spacing } from '../tokens/spacing/scales';

export const getSpacing = (multiplier: number): string => {
  const key = multiplier as keyof typeof spacing;
  return spacing[key] || `${multiplier * 4}px`;
};

export const spacingUtils = {
  p: (value: number) => ({ padding: getSpacing(value) }),
  pt: (value: number) => ({ paddingTop: getSpacing(value) }),
  pr: (value: number) => ({ paddingRight: getSpacing(value) }),
  pb: (value: number) => ({ paddingBottom: getSpacing(value) }),
  pl: (value: number) => ({ paddingLeft: getSpacing(value) }),
  px: (value: number) => ({ paddingLeft: getSpacing(value), paddingRight: getSpacing(value) }),
  py: (value: number) => ({ paddingTop: getSpacing(value), paddingBottom: getSpacing(value) }),
  
  m: (value: number) => ({ margin: getSpacing(value) }),
  mt: (value: number) => ({ marginTop: getSpacing(value) }),
  mr: (value: number) => ({ marginRight: getSpacing(value) }),
  mb: (value: number) => ({ marginBottom: getSpacing(value) }),
  ml: (value: number) => ({ marginLeft: getSpacing(value) }),
  mx: (value: number) => ({ marginLeft: getSpacing(value), marginRight: getSpacing(value) }),
  my: (value: number) => ({ marginTop: getSpacing(value), marginBottom: getSpacing(value) }),
  
  gap: (value: number) => ({ gap: getSpacing(value) }),
};

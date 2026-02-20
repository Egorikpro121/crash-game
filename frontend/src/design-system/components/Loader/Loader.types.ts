export type LoaderVariant = 'spinner' | 'dots' | 'pulse';
export type LoaderSize = 'sm' | 'md' | 'lg';

export interface LoaderProps {
  variant?: LoaderVariant;
  size?: LoaderSize;
  color?: string;
}

/**
 * Card component tests
 */

import React from 'react';
import { render } from '@testing-library/react';
import { Card } from './Card';

describe('Card', () => {
  it('renders correctly', () => {
    const { container } = render(<Card>Card content</Card>);
    expect(container.firstChild).toBeInTheDocument();
  });
  
  it('applies variant styles', () => {
    const { container } = render(<Card variant="elevated">Content</Card>);
    expect(container.firstChild).toHaveStyle({ background: expect.any(String) });
  });
});

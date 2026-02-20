import styled from 'styled-components';
import { zIndex } from '../../tokens/zIndex';
import { colors } from '../../tokens/colors';
import { shadows } from '../../tokens/shadows';
import { radius } from '../../tokens/radius/base';
import { spacing } from '../../tokens/spacing/scales';
import { animation } from '../../tokens/animation';

export const ModalBackdrop = styled.div<{ isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: ${zIndex.modalBackdrop};
  display: ${({ isOpen }) => isOpen ? 'flex' : 'none'};
  align-items: center;
  justify-content: center;
  padding: ${spacing[4]};
  animation: ${({ isOpen }) => isOpen ? 'fadeIn' : 'fadeOut'} ${animation.durations.normal}ms;
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }
`;

const sizeMap = {
  sm: '400px',
  md: '500px',
  lg: '600px',
  xl: '800px',
  full: '100%',
};

export const ModalContainer = styled.div<{ size: string }>`
  background: ${colors.neutral.surface.light};
  border-radius: ${radius['2xl']};
  box-shadow: ${shadows.elevations[5]};
  width: ${({ size }) => sizeMap[size as keyof typeof sizeMap] || sizeMap.md};
  max-width: 100%;
  max-height: 90vh;
  overflow: auto;
  z-index: ${zIndex.modal};
  animation: slideUp ${animation.durations.normal}ms ${animation.easings.easeOut};
  
  @keyframes slideUp {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
`;

export const ModalHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${spacing[6]};
  border-bottom: 1px solid ${colors.neutral.border.medium};
`;

export const ModalBody = styled.div`
  padding: ${spacing[6]};
`;

export const ModalFooter = styled.div`
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: ${spacing[4]};
  padding: ${spacing[6]};
  border-top: 1px solid ${colors.neutral.border.medium};
`;

export const CloseButton = styled.button`
  background: none;
  border: none;
  color: ${colors.neutral.text.secondary};
  cursor: pointer;
  padding: ${spacing[2]};
  border-radius: ${radius.base};
  transition: all ${animation.durations.fast}ms;
  
  &:hover {
    background: ${colors.neutral.surface.medium};
    color: ${colors.neutral.text.primary};
  }
`;

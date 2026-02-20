import React from 'react';
import { ModalBackdrop } from './Modal.styles';

interface BackdropProps {
  isOpen: boolean;
  onClick: () => void;
}

export const Backdrop: React.FC<BackdropProps> = ({ isOpen, onClick }) => {
  return <ModalBackdrop isOpen={isOpen} onClick={onClick} />;
};

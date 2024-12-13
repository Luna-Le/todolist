import type { MessageType } from '../types';

export const showMessage = (text: string, type: MessageType, setMessage: React.Dispatch<React.SetStateAction<{ text: string; type: MessageType }>>) => {
  setMessage({ text, type });
};
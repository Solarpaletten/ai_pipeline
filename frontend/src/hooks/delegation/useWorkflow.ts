import { useState } from 'react';

export const useWorkflow = () => {
  const [status, setStatus] = useState('idle');
  
  return {
    status,
    setStatus
  };
};

export default useWorkflow;

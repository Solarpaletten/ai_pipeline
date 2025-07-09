import { useState } from 'react';

export const useDelegation = () => {
  const [loading, setLoading] = useState(false);
  
  return {
    loading,
    setLoading
  };
};

export default useDelegation;

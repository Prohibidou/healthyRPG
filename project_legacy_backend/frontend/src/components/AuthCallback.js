
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = new URLSearchParams(window.location.search).get('token');
    console.log('Token:', token);
    if (token) {
      localStorage.setItem('authToken', token);
      setTimeout(() => navigate('/profile'), 100);
    } else {
      // Handle the case where the token is not present
      navigate('/');
    }
  }, [navigate]);

  return <div>Loading...</div>;
};

export default AuthCallback;

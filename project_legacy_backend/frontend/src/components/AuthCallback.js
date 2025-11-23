import React, { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const AuthCallback = () => {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  useEffect(() => {
    const token = new URLSearchParams(window.location.search).get('token');
    console.log('Token:', token);
    if (token) {
      login(token);
      setTimeout(() => navigate('/profile'), 100);
    } else {
      // Handle the case where the token is not present
      navigate('/');
    }
  }, [navigate, login]);

  return <div>Loading...</div>;
};

export default AuthCallback;

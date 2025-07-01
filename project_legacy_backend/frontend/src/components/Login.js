import React from 'react';

const Login = () => {
  const handleLogin = () => {
    window.location.href = 'http://localhost:8000/accounts/google/login/?process=login';
  };

  return (
    <div>
      <h2>Login</h2>
      <button onClick={handleLogin}>
        Login with Google
      </button>
    </div>
  );
};

export default Login;

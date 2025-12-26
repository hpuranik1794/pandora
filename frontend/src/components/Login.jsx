import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api';
import { AuthForm } from './AuthForm';

export const Login = () => {
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (username, password) => {
    try {
      const data = await login(username, password);
      localStorage.setItem('token', data.access_token);
      navigate('/chat');
    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <AuthForm
      title="Sign in to your account"
      buttonText="Sign in"
      onSubmit={handleLogin}
      linkText="Don't have an account? Sign up"
      linkTo="/signup"
      error={error}
    />
  );
};

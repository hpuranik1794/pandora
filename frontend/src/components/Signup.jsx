import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from '../api';
import { AuthForm } from './AuthForm';

export const Signup = () => {
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (username, password) => {
    try {
      await signup(username, password);
      navigate('/login');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <AuthForm
      title="Create your account"
      buttonText="Sign up"
      onSubmit={handleSignup}
      linkText="Already have an account? Sign in"
      linkTo="/login"
      error={error}
    />
  );
};

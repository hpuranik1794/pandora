import { useState } from 'react';
import { Link } from 'react-router-dom';

export const AuthForm = ({ title, buttonText, onSubmit, linkText, linkTo, error }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(username, password);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-primary-50 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-md w-full space-y-8">
        <div>
          <Link to="/" className="flex justify-center mb-6">
             <span className="font-serif text-4xl tracking-tight text-primary-800 font-bold">Pandora</span>
          </Link>
          <h2 className="mt-6 text-center text-3xl font-serif text-primary-800">
            {title}
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <input
                type="text"
                required
                className="appearance-none rounded-t-md relative block w-full px-3 py-3 border border-primary-200 placeholder-primary-400 text-primary-900 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm bg-white"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div>
              <input
                type="password"
                required
                className="appearance-none rounded-b-md relative block w-full px-3 py-3 border border-primary-200 placeholder-primary-400 text-primary-900 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm bg-white"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {error && <div className="text-red-500 text-sm text-center bg-red-50 p-2 rounded">{error}</div>}

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-full text-white bg-primary-800 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              {buttonText}
            </button>
          </div>
          <div className="text-center">
            <Link to={linkTo} className="text-primary-600 hover:text-primary-800 font-medium transition-colors">
              {linkText}
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

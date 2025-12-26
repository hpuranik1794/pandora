import { Link } from 'react-router-dom';
import { Heart, Sparkles, MessageCircle } from 'lucide-react';

export function LandingPage() {
  const isLoggedIn = !!localStorage.getItem('token');

  return (
    <div className="min-h-screen bg-primary-50 font-sans text-primary-800">
      {/* nav */}
      <nav className="sticky top-0 z-50 bg-primary-50/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center gap-2">
                <span className="font-serif text-3xl tracking-tight text-primary-800 font-bold">Pandora</span>
              </div>
            </div>
            <div className="flex items-center gap-6">
              {isLoggedIn ? (
                <Link to="/chat" className="bg-primary-800 text-white px-6 py-3 rounded-full font-medium hover:bg-primary-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 flex items-center gap-2">
                  <MessageCircle size={18} />
                  Go to Chat
                </Link>
              ) : (
                <>
                  <Link to="/login" className="text-primary-800 font-medium hover:opacity-70 transition-opacity">Log in</Link>
                  <Link to="/signup" className="bg-primary-800 text-white px-6 py-3 rounded-full font-medium hover:bg-primary-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
                    Get started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>
      
      {/* landing */}
      <div className="relative overflow-hidden pt-16 pb-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl md:text-7xl font-serif text-primary-800 mb-8 leading-tight">
              Your safe space <br/> to just be.
            </h1>
            <p className="mt-4 text-xl md:text-2xl text-primary-700 max-w-2xl mx-auto mb-12 leading-relaxed font-light">
              Pandora is a compassionate AI companion designed to listen, understand, and support your mental well-being journey with complete privacy.
            </p>
            
            <div className="flex justify-center">
              {isLoggedIn ? (
                <Link to="/chat" className="bg-primary-800 text-white px-8 py-4 rounded-full text-lg font-medium hover:bg-primary-700 transition-all shadow-xl hover:shadow-2xl transform hover:-translate-y-1 flex items-center gap-2">
                  <MessageCircle size={20} />
                  Continue Conversation
                </Link>
              ) : (
                <Link to="/signup" className="bg-primary-800 text-white px-8 py-4 rounded-full text-lg font-medium hover:bg-primary-700 transition-all shadow-xl hover:shadow-2xl transform hover:-translate-y-1">
                  Start talking now
                </Link>
              )}
            </div>

            <div className="absolute top-1/4 left-10 hidden lg:block animate-bounce-slow">
                <Sparkles className="w-12 h-12 text-yellow-400 opacity-80" />
            </div>
            <div className="absolute bottom-1/4 right-10 hidden lg:block animate-pulse">
                <Heart className="w-16 h-16 text-pink-300 opacity-60" />
            </div>
        </div>
      </div>

      {/* footer */}
      <footer className="bg-primary-900 border-t border-primary-800 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center gap-2">
          <span className="font-serif text-xl font-bold text-primary-50">Pandora</span>
          <div className="text-primary-200 text-sm flex items-center gap-1">
            Made with <Heart className="w-3 h-3 text-red-400 fill-current" /> by Harsha &copy; 2025
          </div>
        </div>
      </footer>
    </div>
  );
}

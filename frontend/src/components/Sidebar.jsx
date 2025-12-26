import { MessageSquare, Plus, LogOut } from 'lucide-react';
import { twMerge } from 'tailwind-merge';
import { Link, useNavigate } from 'react-router-dom';

export function Sidebar({ conversations, currentConversationId, onSelectConversation, onNewChat, user }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="w-64 bg-white border-r border-primary-200 flex flex-col h-full">
      <div className="p-4 border-b border-primary-200">
        <Link to="/" className="flex items-center gap-2 mb-6 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 bg-primary-800 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">P</span>
            </div>
            <span className="font-bold text-xl text-primary-900">Pandora</span>
        </Link>
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 bg-primary-800 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors shadow-sm"
        >
          <Plus size={20} />
          <span>New Chat</span>
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        <h3 className="px-3 py-2 text-xs font-semibold text-primary-400 uppercase tracking-wider">History</h3>
        {conversations.map((conv, index) => (
          <button
            key={conv.id}
            onClick={() => onSelectConversation(conv.id)}
            className={twMerge(
              "w-full flex items-center gap-3 px-3 py-3 rounded-lg text-left transition-colors",
              currentConversationId === conv.id 
                ? "bg-primary-100 text-primary-900" 
                : "text-primary-700 hover:bg-primary-50"
            )}
          >
            <MessageSquare size={18} className={currentConversationId === conv.id ? "text-primary-800" : "text-primary-400"} />
            <span className="truncate text-sm font-medium">
              {conv.title || `Conversation ${index + 1}`}
            </span>
          </button>
        ))}
      </div>
      
      <div className="p-4 border-t border-primary-200 bg-primary-50/50">
        <div className="flex items-center gap-3 text-primary-700 text-sm">
          <div className="w-8 h-8 rounded-full bg-primary-200 flex items-center justify-center text-primary-800 font-bold border border-primary-300">
            {user ? user.username[0].toUpperCase() : 'U'}
          </div>
          <div className="flex-1 flex justify-between items-center">
            <div className="font-medium">{user ? user.username : 'User'}</div>
            <button onClick={handleLogout} className="text-primary-500 hover:text-primary-800 p-1 rounded hover:bg-primary-100 transition-colors" title="Log out">
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

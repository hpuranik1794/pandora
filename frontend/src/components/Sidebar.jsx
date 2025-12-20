import React from 'react';
import { MessageSquare, Plus, Trash2 } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Sidebar({ conversations, currentConversationId, onSelectConversation, onNewChat }) {
  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col h-full">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-2 mb-6">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">P</span>
            </div>
            <span className="font-bold text-xl text-gray-900">Pandora</span>
        </div>
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors shadow-sm"
        >
          <Plus size={20} />
          <span>New Chat</span>
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        <h3 className="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">History</h3>
        {conversations.map((conv) => (
          <button
            key={conv.id}
            onClick={() => onSelectConversation(conv.id)}
            className={twMerge(
              "w-full flex items-center gap-3 px-3 py-3 rounded-lg text-left transition-colors",
              currentConversationId === conv.id 
                ? "bg-primary-50 text-primary-900" 
                : "text-gray-700 hover:bg-gray-100"
            )}
          >
            <MessageSquare size={18} className={currentConversationId === conv.id ? "text-primary-600" : "text-gray-400"} />
            <span className="truncate text-sm font-medium">
              {conv.title || `Conversation ${conv.id}`}
            </span>
          </button>
        ))}
      </div>
      
      <div className="p-4 border-t border-gray-200 bg-gray-50">
        <div className="flex items-center gap-3 text-gray-500 text-sm">
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-bold border border-primary-200">
            U
          </div>
          <div className="flex-1">
            <p className="font-medium text-gray-900">User</p>
            <p className="text-xs">Pandora Client</p>
          </div>
        </div>
      </div>
    </div>
  );
}

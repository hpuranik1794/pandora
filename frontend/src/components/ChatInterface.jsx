import { useState, useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { ChatArea } from './ChatArea';
import { createConversation, getConversations, getMessages, streamMessage, getMe } from '../api';

export function ChatInterface() {
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    loadUser();
    loadConversations();
  }, []);

  const loadUser = async () => {
    try {
      const userData = await getMe();
      setUser(userData);
    } catch (error) {
      console.error('Failed to load user:', error);
    }
  };

  useEffect(() => {
    if (currentConversationId) {
      loadMessages(currentConversationId);
    } else {
      setMessages([]);
    }
  }, [currentConversationId]);

  const loadConversations = async () => {
    try {
      const data = await getConversations();
      setConversations(data);
      if (data.length > 0 && !currentConversationId) {
        setCurrentConversationId(data[data.length - 1].id);
      }
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const loadMessages = async (id) => {
    try {
      const data = await getMessages(id);
      setMessages(data.messages || []);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const handleNewChat = async () => {
    try {
      const data = await createConversation();
      const newId = data.conversation_id;
      await loadConversations();
      setCurrentConversationId(newId);
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  const handleSendMessage = async (text) => {
    if (!currentConversationId) return;

    const tempMessage = { role: 'user', content: text };
    setMessages(prev => [...prev, tempMessage, { role: 'assistant', content: '' }]);
    setIsLoading(true);

    try {
      await streamMessage(currentConversationId, text, (chunk) => {
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMsgIndex = newMessages.length - 1;
          if (newMessages[lastMsgIndex].role === 'assistant') {
             newMessages[lastMsgIndex] = {
                ...newMessages[lastMsgIndex],
                content: newMessages[lastMsgIndex].content + chunk
             };
          }
          return newMessages;
        });
      });
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full bg-primary-50">
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={setCurrentConversationId}
        onNewChat={handleNewChat}
        user={user}
      />
      <ChatArea
        messages={messages}
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
      />
    </div>
  );
}

const API_BASE = '/api/chat';

export const createConversation = async () => {
  const res = await fetch(`${API_BASE}/conversations`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to create conversation');
  return res.json();
};

export const getConversations = async () => {
  const res = await fetch(`${API_BASE}/conversations`);
  if (!res.ok) throw new Error('Failed to fetch conversations');
  return res.json();
};

export const getMessages = async (conversationId) => {
  const res = await fetch(`${API_BASE}/message/${conversationId}`);
  if (!res.ok) throw new Error('Failed to fetch messages');
  return res.json();
};

export const sendMessage = async (conversationId, userInput) => {
  const res = await fetch(`${API_BASE}/message/${conversationId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_input: userInput }),
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
};

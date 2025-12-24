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

export const streamMessage = async (conversationId, userInput, onChunk) => {
  const response = await fetch(`${API_BASE}/message/${conversationId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_input: userInput }),
  });

  if (!response.ok) throw new Error('Failed to send message');

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const textChunk = decoder.decode(value, { stream: true });
    
    for (const char of textChunk) {
      onChunk(char);
      await new Promise(resolve => setTimeout(resolve, 30));
    }
  }
};

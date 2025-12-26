const API_BASE = '/api';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

export const login = async (username, password) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      body: formData
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}

export const signup = async (username, password) => {
  const res = await fetch(`${API_BASE}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
  });
  if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Signup failed');
  }
  return res.json();
}

export const getMe = async () => {
  const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch user info');
  return res.json();
};

export const createConversation = async () => {
  const res = await fetch(`${API_BASE}/chat/conversations`, { 
      method: 'POST',
      headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to create conversation');
  return res.json();
};

export const getConversations = async () => {
  const res = await fetch(`${API_BASE}/chat/conversations`, {
      headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch conversations');
  return res.json();
};

export const getMessages = async (conversationId) => {
  const res = await fetch(`${API_BASE}/chat/message/${conversationId}`, {
      headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch messages');
  return res.json();
};

export const streamMessage = async (conversationId, userInput, onChunk) => {
  const response = await fetch(`${API_BASE}/chat/message/${conversationId}`, {
    method: 'POST',
    headers: getHeaders(),
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

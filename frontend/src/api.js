const API_BASE = '/api';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
};

const handleResponse = async (res) => {
  if (res.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Request failed');
  }
  return res.json();
};


export const login = async (username, password) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    body: formData
  });

  return handleResponse(res);
}

export const signup = async (username, password) => {
  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  return handleResponse(res);
}

export const getMe = async () => {
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: getHeaders()
  });

  return handleResponse(res);
};

export const createConversation = async () => {
  const res = await fetch(`${API_BASE}/chat/conversations`, { 
    method: 'POST',
    headers: getHeaders()
  });

  return handleResponse(res);
};

export const getConversations = async () => {
  const res = await fetch(`${API_BASE}/chat/conversations`, {
    headers: getHeaders()
  });

  return handleResponse(res);
};

export const getMessages = async (conversationId) => {
  const res = await fetch(`${API_BASE}/chat/message/${conversationId}`, {
    headers: getHeaders()
  });

  return handleResponse(res);
};

export const streamMessage = async (conversationId, userInput, onChunk) => {
  const response = await fetch(`${API_BASE}/chat/message/${conversationId}`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ user_input: userInput }),
  });

  if (response.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }

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

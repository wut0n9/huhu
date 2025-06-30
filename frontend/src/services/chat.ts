import { Message, ChatRequest, ChatResponse } from '@/types/chat';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const chatAPI = {
  // 发送消息
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error('发送消息失败');
    }

    return response.json();
  },

  // 流式发送消息
  async sendMessageStream(request: ChatRequest): Promise<ReadableStream> {
    const response = await fetch(`${API_BASE_URL}/api/v1/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error('发送消息失败');
    }

    return response.body!;
  },

  // 获取对话历史
  async getConversationHistory(conversationId: string): Promise<Message[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/conversations/${conversationId}/messages`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    if (!response.ok) {
      throw new Error('获取对话历史失败');
    }

    return response.json();
  },

  // 获取对话列表
  async getConversations(): Promise<any[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/conversations`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    if (!response.ok) {
      throw new Error('获取对话列表失败');
    }

    return response.json();
  }
}; 
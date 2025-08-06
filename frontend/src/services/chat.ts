import { Message, ChatRequest, ChatResponse, StreamChatResponse } from '@/types/chat';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const chatAPI = {
  // 发送消息（非流式）
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/agent/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...request,
        stream: false
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '发送消息失败');
    }

    return response.json();
  },

  // 流式发送消息
  async sendMessageStream(
    request: ChatRequest,
    onChunk: (chunk: StreamChatResponse) => void,
    onError?: (error: Error) => void,
    onComplete?: () => void,
    abortController?: AbortController
  ): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify({
          ...request,
          stream: true
        }),
        signal: abortController?.signal
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || '发送消息失败');
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法获取响应流');
      }

      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // 使用流式解码，避免不完整的UTF-8字符
        const chunk = decoder.decode(value, { stream: true });
        // 按照SSE标准，使用双换行符分割消息
        const messages = chunk.split('\n\n');
        console.log("message:", messages)

        for (const message of messages) {
          if (!message.trim()) continue;

          // 每个message已经是完整的SSE消息，直接处理
          const trimmedMessage = message.trim();
          if (trimmedMessage.startsWith('data: ')) {
            try {
              const jsonStr = trimmedMessage.slice(6).trim();
              if (jsonStr === '[DONE]') {
                onComplete?.();
                return;
              }

              const data = JSON.parse(jsonStr);
              console.log('成功解析流式数据:', data);
              onChunk(data);

              if (data.is_final) {
                onComplete?.();
                return;
              }
            } catch (e) {
              console.error('解析流式响应失败:', e, '原始数据:', trimmedMessage);
            }
          }
        }
      }

      onComplete?.();
    } catch (error) {
      console.error('流式请求错误:', error);
      onError?.(error as Error);
      throw error;
    }
  },

  // 获取对话历史
  async getConversationHistory(conversationId: string): Promise<Message[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/agent/conversations/${conversationId}/history`);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取对话历史失败');
    }

    return response.json();
  },

  // 清除对话历史
  async clearConversationHistory(conversationId: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/v1/agent/conversations/${conversationId}`, {
      method: 'DELETE'
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '清除对话历史失败');
    }
  },

  // 获取MCP服务器列表
  async getMCPServers(): Promise<any[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/agent/mcp/servers`);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取MCP服务器列表失败');
    }

    return response.json();
  },

  // 获取可用工具列表
  async getAvailableTools(): Promise<any[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/agent/mcp/tools`);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || '获取工具列表失败');
    }

    return response.json();
  }
};
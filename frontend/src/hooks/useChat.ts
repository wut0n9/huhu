import { useState, useCallback, useEffect } from 'react';
import { Message, ChatState, MCPTool, Conversation, UploadedFile } from '@/types/chat';
import { generateId } from '@/utils/helpers';

// Mock数据
const MOCK_CONVERSATIONS: Conversation[] = [
  {
    id: '1',
    title: '关于项目架构的讨论',
    messages: [
      {
        id: '1',
        role: 'user',
        content: '请介绍一下这个项目的整体架构',
        timestamp: '2024-01-15T10:00:00Z',
        conversationId: '1'
      },
      {
        id: '2',
        role: 'assistant',
        content: '这个项目采用前后端分离的架构，前端使用React+TypeScript+Ant Design，后端使用FastAPI+Python。前端负责用户界面和交互，后端提供API接口和业务逻辑处理。',
        timestamp: '2024-01-15T10:01:00Z',
        conversationId: '1'
      }
    ],
    createdAt: '2024-01-15T10:00:00Z',
    updatedAt: '2024-01-15T10:01:00Z'
  },
  {
    id: '2',
    title: '数据库设计问题',
    messages: [
      {
        id: '3',
        role: 'user',
        content: '数据库表结构应该如何设计？',
        timestamp: '2024-01-16T14:00:00Z',
        conversationId: '2'
      }
    ],
    createdAt: '2024-01-16T14:00:00Z',
    updatedAt: '2024-01-16T14:00:00Z'
  }
];

const useChat = () => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    conversationId: null,
    isLoading: false,
    selectedMCPTools: [],
    uploadedFiles: [],
    conversations: [],
    currentStreamingMessage: null,
    streamingIndex: 0
  });

  // 流式递增 useEffect
  useEffect(() => {
    if (
      state.currentStreamingMessage &&
      state.streamingIndex < state.currentStreamingMessage.length
    ) {
      const timer = setTimeout(() => {
        setState(prev => ({
          ...prev,
          streamingIndex: prev.streamingIndex + 1
        }));
      }, 50);
      return () => clearTimeout(timer);
    }
    // 流式结束，写入完整 assistant 消息
    if (
      state.currentStreamingMessage &&
      state.streamingIndex === state.currentStreamingMessage.length
    ) {
      const assistantMessage = {
        id: generateId(),
        role: 'assistant' as const,
        content: state.currentStreamingMessage,
        timestamp: new Date().toISOString(),
        conversationId: state.conversationId || 'new'
      };
      setState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        currentStreamingMessage: null,
        streamingIndex: 0,
        isLoading: false
      }));
    }
  }, [state.currentStreamingMessage, state.streamingIndex]);

  // 加载对话列表
  const loadConversations = useCallback(async () => {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 500));
    
    setState(prev => ({
      ...prev,
      conversations: MOCK_CONVERSATIONS
    }));
  }, []);

  // 发送消息
  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    const newMessage: Message = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
      conversationId: state.conversationId || 'new'
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, newMessage],
      isLoading: true
    }));

    // 模拟流式输出
    const response = `这是对"${content}"的回复。我正在模拟流式响应，这个回复会逐字显示。`;
    setState(prev => ({
      ...prev,
      currentStreamingMessage: response,
      streamingIndex: 1 // 立即显示第一个字符
    }));
  }, [state.conversationId]);

  // 选择MCP工具
  const selectMCPTool = useCallback((tool: MCPTool) => {
    setState(prev => ({
      ...prev,
      selectedMCPTools: [...prev.selectedMCPTools, tool]
    }));
  }, []);

  // 移除MCP工具
  const removeMCPTool = useCallback((toolId: string) => {
    setState(prev => ({
      ...prev,
      selectedMCPTools: prev.selectedMCPTools.filter(tool => tool.id !== toolId)
    }));
  }, []);

  // 上传文件
  const uploadFile = useCallback(async (file: File): Promise<UploadedFile> => {
    // 模拟文件上传
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const uploadedFile: UploadedFile = {
      file_id: generateId(),
      filename: file.name,
      size: file.size
    };

    setState(prev => ({
      ...prev,
      uploadedFiles: [...prev.uploadedFiles, uploadedFile]
    }));

    return uploadedFile;
  }, []);

  // 移除文件
  const removeFile = useCallback((fileId: string) => {
    setState(prev => ({
      ...prev,
      uploadedFiles: prev.uploadedFiles.filter(file => file.file_id !== fileId)
    }));
  }, []);

  // 切换对话
  const switchConversation = useCallback((conversationId: string) => {
    const conversation = state.conversations.find(c => c.id === conversationId);
    if (conversation) {
      setState(prev => ({
        ...prev,
        conversationId,
        messages: conversation.messages
      }));
    }
  }, [state.conversations]);

  // 清除对话
  const clearConversation = useCallback(async (conversationId: string) => {
    setState(prev => {
      const newConversations = prev.conversations.filter(c => c.id !== conversationId);
      // 如果删除的是当前激活会话，重置聊天区
      const isCurrent = prev.conversationId === conversationId;
      return {
        ...prev,
        conversations: newConversations,
        messages: isCurrent ? [] : prev.messages,
        conversationId: isCurrent ? null : prev.conversationId,
        selectedMCPTools: isCurrent ? [] : prev.selectedMCPTools,
        uploadedFiles: isCurrent ? [] : prev.uploadedFiles,
        currentStreamingMessage: isCurrent ? null : prev.currentStreamingMessage,
        streamingIndex: isCurrent ? 0 : prev.streamingIndex
      };
    });
  }, []);

  // 停止流式响应
  const stopStreaming = useCallback(() => {
    setState(prev => ({
      ...prev,
      currentStreamingMessage: null,
      isLoading: false
    }));
  }, []);

  // 新建对话
  const newConversation = useCallback(() => {
    setState(prev => {
      // 仅当当前聊天区有内容时归档
      let newConversations = prev.conversations;
      if (prev.messages.length > 0) {
        const now = new Date();
        const title = prev.messages[0].content.slice(0, 20) || `新会话${now.toLocaleString()}`;
        const newConv = {
          id: generateId(),
          title,
          messages: prev.messages,
          createdAt: prev.messages[0].timestamp,
          updatedAt: prev.messages[prev.messages.length - 1].timestamp
        };
        newConversations = [...prev.conversations, newConv];
      }
      return {
        ...prev,
        conversations: newConversations,
        messages: [],
        conversationId: generateId(),
        selectedMCPTools: [],
        uploadedFiles: [],
        currentStreamingMessage: null,
        streamingIndex: 0
      };
    });
  }, []);

  return {
    ...state,
    sendMessage,
    selectMCPTool,
    removeMCPTool,
    uploadFile,
    removeFile,
    switchConversation,
    clearConversation,
    loadConversations,
    stopStreaming,
    newConversation
  };
};

export default useChat; 
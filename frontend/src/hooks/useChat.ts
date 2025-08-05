import { useState, useCallback, useEffect, useRef } from 'react';
import { Message, ChatState, MCPTool, UploadedFile } from '@/types/chat';
import { generateId } from '@/utils/helpers';
import { chatAPI } from '@/services/chat';

const useChat = () => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    conversationId: null,
    isLoading: false,
    selectedMCPTools: [],
    uploadedFiles: [],
    conversations: [],
    currentStreamingMessage: null
  });

  // 用于中断流式响应的引用
  const abortControllerRef = useRef<AbortController | null>(null);

  // 移除人工逐字符显示效果，直接实时显示流式内容

  // 当流式消息完成时，将其添加到消息列表
  useEffect(() => {
    if (
      state.currentStreamingMessage &&
      !state.isLoading
    ) {
      const assistantMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: state.currentStreamingMessage,
        timestamp: new Date().toISOString(),
        conversationId: state.conversationId || 'new'
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        currentStreamingMessage: null
      }));
    }
  }, [state.currentStreamingMessage, state.isLoading, state.conversationId]);

  // 加载对话列表
  const loadConversations = useCallback(async () => {
    try {
      // 目前后端没有提供对话列表接口，暂时使用空数组
      // 可以根据需要实现本地存储的对话历史
      setState(prev => ({
        ...prev,
        conversations: []
      }));
    } catch (error) {
      console.error('加载对话列表失败:', error);
    }
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
      isLoading: true,
      currentStreamingMessage: null
    }));

    try {
      // 创建新的 AbortController
      const abortController = new AbortController();
      abortControllerRef.current = abortController;

      // 构建MCP服务器配置
      const mcpServers = state.selectedMCPTools.map(tool => ({
        server_name: tool.name,
        server_url: tool.id // 假设tool.id包含服务器URL
      }));

      // 使用流式API
      await chatAPI.sendMessageStream(
        {
          message: content,
          conversation_id: state.conversationId || undefined,
          mcp_servers: mcpServers.length > 0 ? mcpServers : undefined
        },
        (chunk) => {
          // 处理流式响应块
          console.log('收到流式数据块:', chunk);
          setState(prev => ({
            ...prev,
            currentStreamingMessage: (prev.currentStreamingMessage || '') + chunk.content,
            conversationId: chunk.conversation_id
          }));
        },
        (error) => {
          console.error('流式响应错误:', error);
          setState(prev => ({
            ...prev,
            isLoading: false,
            currentStreamingMessage: null
          }));
        },
        () => {
          // 流式响应完成
          setState(prev => ({
            ...prev,
            isLoading: false
          }));
          // 清除 AbortController 引用
          abortControllerRef.current = null;
        },
        abortController
      );
    } catch (error) {
      console.error('发送消息失败:', error);
      setState(prev => ({
        ...prev,
        isLoading: false,
        currentStreamingMessage: null
      }));
      // 清除 AbortController 引用
      abortControllerRef.current = null;
    }
  }, [state.conversationId, state.selectedMCPTools]);

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
  const switchConversation = useCallback(async (conversationId: string) => {
    try {
      setState(prev => ({
        ...prev,
        conversationId,
        messages: [],
        isLoading: true
      }));

      // 获取对话历史
      const messages = await chatAPI.getConversationHistory(conversationId);
      setState(prev => ({
        ...prev,
        messages,
        isLoading: false
      }));
    } catch (error) {
      console.error('切换对话失败:', error);
      setState(prev => ({
        ...prev,
        isLoading: false
      }));
    }
  }, []);

  // 清除对话
  const clearConversation = useCallback(async (conversationId: string) => {
    try {
      await chatAPI.clearConversationHistory(conversationId);

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
          currentStreamingMessage: isCurrent ? null : prev.currentStreamingMessage
        };
      });
    } catch (error) {
      console.error('清除对话失败:', error);
    }
  }, []);

  // 停止流式响应
  const stopStreaming = useCallback(() => {
    // 中断当前请求
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }

    setState(prev => ({
      ...prev,
      isLoading: false
    }));
  }, []);

  // 新建对话
  const newConversation = useCallback(() => {
    setState(prev => ({
      ...prev,
      messages: [],
      conversationId: null, // 新对话不设置ID，让后端自动生成
      selectedMCPTools: [],
      uploadedFiles: [],
      currentStreamingMessage: null,
      isLoading: false
    }));
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
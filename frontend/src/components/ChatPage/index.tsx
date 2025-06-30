import React, { useEffect, useRef } from 'react';
import { ConfigProvider } from 'antd';
import useChat from '@/hooks/useChat';
import useAuth from '@/hooks/useAuth';
import ChatHistory from './ChatHistory';
import ChatInput from './ChatInput';
import MessageItem from './MessageItem';
import UserInfo from './UserInfo';
import Loading from '../common/Loading';
import { THEME_CONFIG } from '@/utils/constants';
import { Message } from '@/types/chat';
import './index.css';

const ChatPage: React.FC = () => {
  const {
    messages,
    conversationId,
    isLoading,
    selectedMCPTools,
    uploadedFiles,
    conversations,
    currentStreamingMessage,
    streamingIndex,
    sendMessage,
    selectMCPTool,
    removeMCPTool,
    uploadFile,
    removeFile,
    switchConversation,
    clearConversation,
    loadConversations,
    stopStreaming,
    newConversation,
  } = useChat();

  const { isLoading: authLoading } = useAuth();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentStreamingMessage]);

  // 加载对话列表
  useEffect(() => {
    // 直接加载对话列表，不需要验证登录状态
    loadConversations();
  }, [loadConversations]);

  // 处理新建对话
  const handleNewConversation = () => {
    newConversation();
  };

  // 处理对话选择
  const handleConversationSelect = (conversationId: string) => {
    switchConversation(conversationId);
  };

  // 处理清除对话
  const handleClearConversation = async (conversationId: string) => {
    await clearConversation(conversationId);
  };

  // 如果正在加载认证状态，显示加载页面
  if (authLoading) {
    return <Loading fullScreen text="正在加载..." />;
  }

  return (
    <ConfigProvider theme={THEME_CONFIG}>
      <div className="chat-page">
        <div className="chat-layout">
          {/* 左侧对话历史 */}
          <ChatHistory
            conversations={conversations}
            currentConversationId={conversationId}
            onConversationSelect={handleConversationSelect}
            onNewConversation={handleNewConversation}
            onClearConversation={handleClearConversation}
            loading={false}
          />

          {/* 右侧聊天区域 */}
          <div className="chat-main">
            {/* 消息区域 */}
            <div className="chat-messages">
              {messages.length === 0 ? (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: '100%',
                  color: '#999',
                  fontSize: '16px'
                }}>
                  开始新的对话吧！
                </div>
              ) : (
                <>
                  {messages.map((message: Message) => (
                    <MessageItem
                      key={message.id}
                      message={message}
                    />
                  ))}
                  
                  {/* 流式消息 */}
                  {currentStreamingMessage && streamingIndex > 0 && (
                    <MessageItem
                      message={{
                        id: 'streaming',
                        role: 'assistant',
                        content: currentStreamingMessage.slice(0, streamingIndex),
                        timestamp: new Date().toISOString(),
                        conversationId: conversationId || 'new',
                      }}
                      isStreaming={true}
                    />
                  )}
                </>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* 底部输入区域 */}
            <ChatInput
              onSendMessage={sendMessage}
              onFileUpload={async (file) => {
                await uploadFile(file);
              }}
              onFileRemove={removeFile}
              onToolSelect={selectMCPTool}
              onToolRemove={removeMCPTool}
              uploadedFiles={uploadedFiles}
              selectedTools={selectedMCPTools}
              isLoading={isLoading}
              onStopStreaming={stopStreaming}
            />
          </div>

          {/* 左下角用户信息 */}
          <div className="user-info-fixed">
            <UserInfo />
          </div>
        </div>
      </div>
    </ConfigProvider>
  );
};

export default ChatPage; 
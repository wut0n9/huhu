import React, { useState, useEffect, useCallback } from 'react';
import { List, Button, Popconfirm, Empty, Spin, Input, message } from 'antd';
import { PlusOutlined, DeleteOutlined, MessageOutlined, SearchOutlined } from '@ant-design/icons';
import { Conversation } from '@/types/chat';
import { formatTime } from '@/utils/helpers';
import './index.css';

const { Search } = Input;

interface ChatHistoryProps {
  conversations: Conversation[];
  currentConversationId: string | null;
  onConversationSelect: (conversationId: string) => void;
  onNewConversation: () => void;
  onClearConversation: (conversationId: string) => void;
  loading?: boolean;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({
  conversations,
  currentConversationId,
  onConversationSelect,
  onNewConversation,
  onClearConversation,
  loading = false,
}) => {
  const [searchText, setSearchText] = useState('');
  const [filteredConversations, setFilteredConversations] = useState<Conversation[]>(conversations);

  // 过滤对话
  useEffect(() => {
    if (!searchText.trim()) {
      setFilteredConversations(conversations);
    } else {
      const filtered = conversations.filter(conversation =>
        conversation.title.toLowerCase().includes(searchText.toLowerCase()) ||
        (conversation.messages.length > 0 && 
         conversation.messages[conversation.messages.length - 1].content.toLowerCase().includes(searchText.toLowerCase()))
      );
      setFilteredConversations(filtered);
    }
  }, [conversations, searchText]);

  // 处理对话选择
  const handleConversationSelect = useCallback((conversationId: string) => {
    onConversationSelect(conversationId);
  }, [onConversationSelect]);

  // 处理清除对话
  const handleClearConversation = useCallback(async (conversationId: string) => {
    try {
      await onClearConversation(conversationId);
      message.success('对话已清除');
    } catch (error) {
      message.error('清除对话失败');
    }
  }, [onClearConversation]);

  // 获取对话图标
  const getConversationIcon = (conversation: Conversation) => {
    if (conversation.messages.length === 0) {
      return <MessageOutlined style={{ color: '#d9d9d9' }} />;
    }
    return <MessageOutlined style={{ color: '#1890ff' }} />;
  };

  // 获取最后一条消息
  const getLastMessage = (conversation: Conversation) => {
    if (conversation.messages.length === 0) return '暂无消息';
    const lastMessage = conversation.messages[conversation.messages.length - 1];
    return lastMessage.content.length > 30 
      ? lastMessage.content.substring(0, 30) + '...' 
      : lastMessage.content;
  };

  // 渲染对话项
  const renderConversationItem = (conversation: Conversation) => {
    const isActive = conversation.id === currentConversationId;
    
    return (
      <List.Item
        style={{
          padding: '8px 12px',
          cursor: 'pointer',
          borderRadius: '6px',
          backgroundColor: isActive ? '#e6f7ff' : 'transparent',
          border: isActive ? '1px solid #91d5ff' : '1px solid transparent',
          marginBottom: '4px',
        }}
        onClick={() => handleConversationSelect(conversation.id)}
        actions={[
          <Popconfirm
            key="delete"
            title="确定要清除这个对话吗？"
            onConfirm={() => onClearConversation(conversation.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button
              type="text"
              size="small"
              icon={<DeleteOutlined />}
              onClick={(e) => e.stopPropagation()}
              style={{ color: '#ff4d4f' }}
            />
          </Popconfirm>
        ]}
      >
        <List.Item.Meta
          avatar={getConversationIcon(conversation)}
          title={
            <div style={{ 
              fontWeight: isActive ? 600 : 400,
              color: isActive ? '#1890ff' : '#333',
              fontSize: '14px',
              lineHeight: '1.4',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap'
            }}>
              {conversation.title || '新对话'}
            </div>
          }
          description={
            <div>
              <div style={{
                fontSize: '12px',
                color: '#666',
                lineHeight: '1.3',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
                marginBottom: '2px'
              }}>
                {getLastMessage(conversation)}
              </div>
              <div style={{
                fontSize: '11px',
                color: '#999',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <span>{formatTime(conversation.updatedAt)}</span>
                {conversation.messages.length > 0 && (
                  <span style={{
                    backgroundColor: '#f0f0f0',
                    padding: '1px 6px',
                    borderRadius: '10px',
                    fontSize: '10px'
                  }}>
                    {conversation.messages.length}
                  </span>
                )}
              </div>
            </div>
          }
        />
      </List.Item>
    );
  };

  return (
    <div className="chat-sidebar">
      {/* 头部 */}
      <div style={{
        padding: '16px',
        borderBottom: '1px solid #f0f0f0',
        background: '#ffffff'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '12px'
        }}>
          <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>
            对话历史
          </h3>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            size="small"
            onClick={onNewConversation}
          >
            新建
          </Button>
        </div>
        
        <Search
          placeholder="搜索对话..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          prefix={<SearchOutlined />}
          allowClear
          size="small"
        />
      </div>

      {/* 对话列表 */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        {loading ? (
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            height: '200px'
          }}>
            <Spin />
          </div>
        ) : filteredConversations.length > 0 ? (
          <div style={{ 
            padding: '8px',
            height: '100%',
            overflowY: 'auto'
          }}>
            <List
              dataSource={filteredConversations}
              renderItem={renderConversationItem}
              size="small"
            />
          </div>
        ) : (
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description={
              searchText ? '没有找到匹配的对话' : '暂无对话记录'
            }
            style={{
              margin: '40px 20px',
              fontSize: '14px'
            }}
          />
        )}
      </div>
    </div>
  );
};

export default ChatHistory; 
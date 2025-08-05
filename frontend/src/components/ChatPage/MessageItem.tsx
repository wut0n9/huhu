import React from 'react';
import { Avatar, Tooltip } from 'antd';
import { UserOutlined, RobotOutlined, ToolOutlined } from '@ant-design/icons';
import { Message } from '@/types/chat';
import { formatTime } from '@/utils/helpers';
import './MessageItem.css';
import { Bubble } from '@ant-design/x';

interface MessageItemProps {
  message: Message;
  isStreaming?: boolean;
}

const MessageItem: React.FC<MessageItemProps> = ({ message, isStreaming = false }) => {
  const getAvatar = () => {
    switch (message.role) {
      case 'user':
        return <UserOutlined />;
      case 'assistant':
        return <RobotOutlined />;
      case 'tool':
        return <ToolOutlined />;
      default:
        return <UserOutlined />;
    }
  };

  const getAvatarColor = () => {
    switch (message.role) {
      case 'user':
        return '#1890ff';
      case 'assistant':
        return '#52c41a';
      case 'tool':
        return '#fa8c16';
      default:
        return '#1890ff';
    }
  };

  const renderContent = () => {
    if (message.toolCalls && message.toolCalls.length > 0) {
      return (
        <div className="tool-call">
          <div className="tool-call-header">
            <ToolOutlined />
            <span>工具调用</span>
          </div>
          {message.toolCalls.map((toolCall, index) => (
            <div key={index} className="tool-call-content">
              <div><strong>工具:</strong> {toolCall.function.name}</div>
              <div><strong>参数:</strong> {toolCall.function.arguments}</div>
            </div>
          ))}
        </div>
      );
    }

    if (message.role === 'assistant') {
      return (
        <Bubble
          content={message.content}
          typing={false}  // 禁用打字机效果，直接显示服务器返回的原始片段
          placement="start"
        />
      );
    }

    return (
      <div className="message-content">
        {message.content}
        {isStreaming && <span className="loading-dots"></span>}
      </div>
    );
  };

  return (
    <div className={`message-item ${message.role}`}>
      {message.role === 'assistant' && (
        <Avatar 
          icon={getAvatar()} 
          style={{ backgroundColor: getAvatarColor(), marginRight: 8 }}
        />
      )}
      
      <div className="message-wrapper">
        {renderContent()}
        <div className="message-time">
          <Tooltip title={new Date(message.timestamp).toLocaleString('zh-CN')}>
            {formatTime(message.timestamp)}
          </Tooltip>
        </div>
      </div>
      
      {message.role === 'user' && (
        <Avatar 
          icon={getAvatar()} 
          style={{ backgroundColor: getAvatarColor(), marginLeft: 8 }}
        />
      )}
    </div>
  );
};

export default MessageItem; 
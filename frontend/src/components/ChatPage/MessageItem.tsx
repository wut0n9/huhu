import React from 'react';
import { Avatar, Tooltip } from 'antd';
import { UserOutlined, RobotOutlined, ToolOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Message } from '@/types/chat';
import { formatTime } from '@/utils/helpers';
import './MessageItem.css';

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
        <div className="message-content assistant-bubble">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={{
              code(props: any) {
                const { node, inline, className, children, ...rest } = props;
                const match = /language-(\w+)/.exec(className || '');
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={tomorrow as any}
                    language={match[1]}
                    PreTag="div"
                    {...rest}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...rest}>
                    {children}
                  </code>
                );
              },
              // 自定义链接渲染，确保安全性
              a({ href, children, ...props }) {
                return (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    {...props}
                  >
                    {children}
                  </a>
                );
              },
              // 自定义表格样式
              table({ children, ...props }) {
                return (
                  <div className="markdown-table-wrapper">
                    <table {...props}>{children}</table>
                  </div>
                );
              },
              // 自定义有序列表渲染 - 完全禁用自动序号
              ol({ children, className, ...props }: any) {
                return (
                  <div className={`markdown-ordered-list ${className || ''}`}>
                    {children}
                  </div>
                );
              },
              // 自定义无序列表渲染 - 完全禁用项目符号
              ul({ children, className, ...props }: any) {
                return (
                  <div className={`markdown-unordered-list ${className || ''}`}>
                    {children}
                  </div>
                );
              },
              // 自定义列表项渲染 - 不添加任何额外标记
              li({ children, className, ...props }: any) {
                return (
                  <div className={`markdown-list-item ${className || ''}`}>
                    {children}
                  </div>
                );
              }
            }}
          >
            {message.content}
          </ReactMarkdown>
          {isStreaming && <span className="loading-dots"></span>}
        </div>
      );
    }

    return (
      <div className="message-content">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
          components={{
            code(props: any) {
              const { node, inline, className, children, ...rest } = props;
              const match = /language-(\w+)/.exec(className || '');
              return !inline && match ? (
                <SyntaxHighlighter
                  style={tomorrow as any}
                  language={match[1]}
                  PreTag="div"
                  {...rest}
                >
                  {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
              ) : (
                <code className={className} {...rest}>
                  {children}
                </code>
              );
            },
            a({ href, children, ...props }) {
              return (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props}
                >
                  {children}
                </a>
              );
            },
            // 自定义有序列表渲染 - 完全禁用自动序号
            ol({ children, className }: any) {
              return (
                <div className={`markdown-ordered-list ${className || ''}`}>
                  {children}
                </div>
              );
            },
            // 自定义无序列表渲染 - 完全禁用项目符号
            ul({ children, className }: any) {
              return (
                <div className={`markdown-unordered-list ${className || ''}`}>
                  {children}
                </div>
              );
            },
            // 自定义列表项渲染 - 不添加任何额外标记
            li({ children, className }: any) {
              return (
                <div className={`markdown-list-item ${className || ''}`}>
                  {children}
                </div>
              );
            }
          }}
        >
          {message.content}
        </ReactMarkdown>
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
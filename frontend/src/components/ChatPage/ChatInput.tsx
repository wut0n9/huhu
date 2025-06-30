import React, { useState, useRef, useCallback } from 'react';
import { Input, Button, Tooltip, Space, Tag, Progress } from 'antd';
import { SendOutlined, StopOutlined } from '@ant-design/icons';
import { MCPTool, UploadedFile } from '@/types/chat';
import MCPToolSelector from './MCPToolSelector';
import FileUpload from './FileUpload';
import './index.css';

const { TextArea } = Input;

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  onFileUpload: (file: File) => Promise<void>;
  onFileRemove: (fileId: string) => void;
  onToolSelect: (tool: MCPTool) => void;
  onToolRemove: (toolId: string) => void;
  uploadedFiles: UploadedFile[];
  selectedTools: MCPTool[];
  isLoading: boolean;
  onStopStreaming: () => void;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  onFileUpload,
  onFileRemove,
  onToolSelect,
  onToolRemove,
  uploadedFiles,
  selectedTools,
  isLoading,
  onStopStreaming,
}) => {
  const [message, setMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // 发送消息
  const handleSend = useCallback(() => {
    if (!message.trim() || isLoading) return;
    
    onSendMessage(message.trim());
    setMessage('');
    
    // 重置输入框高度
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  }, [message, isLoading, onSendMessage]);

  // 处理按键事件
  const handleKeyPress = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  // 处理文件上传
  const handleFileUpload = useCallback(async (file: File) => {
    setIsUploading(true);
    try {
      await onFileUpload(file);
    } catch (error) {
      console.error('文件上传失败:', error);
    } finally {
      setIsUploading(false);
    }
  }, [onFileUpload]);

  // 自动调整输入框高度
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    // 自动调整高度
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
  }, []);

  return (
    <div className="chat-input-area">
      {/* 已上传的文件 */}
      {uploadedFiles.length > 0 && (
        <div style={{ marginBottom: '8px' }}>
          <Space wrap>
            {uploadedFiles.map((file) => (
              <Tag
                key={file.file_id}
                closable
                onClose={() => onFileRemove(file.file_id)}
                style={{ margin: 0 }}
              >
                📎 {file.filename}
              </Tag>
            ))}
          </Space>
        </div>
      )}

      {/* 输入区域 */}
      <div className="chat-input-container">
        <TextArea
          ref={textareaRef}
          className="chat-input"
          value={message}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="输入消息... (Shift + Enter 换行)"
          autoSize={{ minRows: 5, maxRows: 10 }}
          disabled={isLoading}
        />
        
        <div className="chat-input-buttons">
          {/* 文件上传 */}
          <FileUpload
            onFileUpload={handleFileUpload}
            uploadedFiles={uploadedFiles}
            onFileRemove={onFileRemove}
          />

          {/* MCP工具选择 */}
          <MCPToolSelector
            onToolSelect={onToolSelect}
            onToolRemove={onToolRemove}
            selectedTools={selectedTools}
          />

          {/* 发送/停止按钮 */}
          {isLoading ? (
            <Tooltip title="停止生成">
              <Button
                type="primary"
                icon={<StopOutlined />}
                onClick={onStopStreaming}
                danger
                size="small"
              />
            </Tooltip>
          ) : (
            <Tooltip title="发送消息 (Enter)">
              <Button
                type="primary"
                icon={<SendOutlined />}
                onClick={handleSend}
                disabled={!message.trim()}
                size="small"
              />
            </Tooltip>
          )}
        </div>
      </div>

      {/* 上传进度 */}
      {isUploading && (
        <div style={{ marginTop: '8px' }}>
          <Progress percent={50} size="small" status="active" />
        </div>
      )}
    </div>
  );
};

export default ChatInput; 
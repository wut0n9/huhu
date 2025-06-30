import type { ThemeConfig } from 'antd';

// API配置
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// 聊天相关常量
export const MAX_MESSAGE_LENGTH = 4000;
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
export const SUPPORTED_FILE_TYPES = [
  'text/plain',
  'text/markdown',
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/csv',
  'application/json',
];

// 消息类型
export const MESSAGE_TYPES = {
  USER: 'user',
  ASSISTANT: 'assistant',
  TOOL: 'tool',
  SYSTEM: 'system',
} as const;

// 工具调用相关
export const MAX_TOOL_ROUNDS = 5;
export const TOOL_CALL_TIMEOUT = 30000; // 30秒

// 本地存储键名
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_INFO: 'user_info',
  CHAT_HISTORY: 'chat_history',
  SELECTED_TOOLS: 'selected_tools',
} as const;

// 主题配置
export const THEME_CONFIG: ThemeConfig = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 8,
    fontSize: 14,
  }
}; 
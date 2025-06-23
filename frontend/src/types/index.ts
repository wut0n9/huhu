// 用户相关类型
export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  avatar_url?: string
  phone?: string
  preferences?: Record<string, any>
  created_at: string
  updated_at?: string
  last_login?: string
}

export interface UserCreate {
  username: string
  email: string
  password: string
  full_name?: string
  phone?: string
}

export interface UserLogin {
  username: string
  password: string
}

export interface UserUpdate {
  username?: string
  email?: string
  full_name?: string
  phone?: string
  avatar_url?: string
  preferences?: Record<string, any>
}

// Agent相关类型
export interface Agent {
  id: number
  name: string
  description?: string
  agent_type: 'chat' | 'task' | 'workflow' | 'custom'
  status: 'idle' | 'running' | 'paused' | 'error' | 'stopped'
  model_config: Record<string, any>
  system_prompt?: string
  parameters?: Record<string, any>
  user_id: number
  total_conversations: number
  total_tokens_used: number
  last_activity?: string
  created_at: string
  updated_at?: string
}

export interface AgentCreate {
  name: string
  description?: string
  agent_type: 'chat' | 'task' | 'workflow' | 'custom'
  system_prompt?: string
  parameters?: Record<string, any>
  model_config: Record<string, any>
}

export interface AgentUpdate {
  name?: string
  description?: string
  agent_type?: 'chat' | 'task' | 'workflow' | 'custom'
  system_prompt?: string
  parameters?: Record<string, any>
  model_config?: Record<string, any>
}

// 对话相关类型
export interface Conversation {
  id: number
  title?: string
  status: 'active' | 'archived' | 'deleted'
  user_id: number
  agent_id: number
  message_count: number
  total_tokens: number
  created_at: string
  updated_at?: string
}

export interface Message {
  id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  conversation_id: number
  metadata?: Record<string, any>
  tokens_used: number
  created_at: string
}

export interface ConversationWithMessages extends Conversation {
  messages: Message[]
}

export interface ChatRequest {
  message: string
  conversation_id?: number
  agent_id: number
}

export interface ChatResponse {
  message: Message
  conversation_id: number
  tokens_used: number
  response_time: number
}

// API响应类型
export interface ApiResponse<T = any> {
  data?: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
} 
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'tool' | 'system';
  content: string;
  timestamp: string;
  conversationId: string;
  toolCalls?: ToolCall[];
  toolCallId?: string;
  name?: string;
}

export interface ToolCall {
  id: string;
  type: 'function';
  function: {
    name: string;
    arguments: string;
  };
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
  updatedAt: string;
}

export interface MCPTool {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
}

export interface UploadedFile {
  file_id: string;
  filename: string;
  size: number;
}

export interface ChatState {
  messages: Message[];
  conversationId: string | null;
  isLoading: boolean;
  selectedMCPTools: MCPTool[];
  uploadedFiles: UploadedFile[];
  conversations: Conversation[];
  currentStreamingMessage: string | null;
  streamingIndex: number;
}

export interface ChatRequest {
  message: string;
  conversationId?: string;
  stream?: boolean;
  mcpServers?: Array<{
    serverName: string;
    serverUrl: string;
  }>;
}

export interface ChatResponse {
  conversationId: string;
  message: string;
  toolCalls?: any[];
  usage?: any;
}

export interface StreamChatResponse {
  conversationId: string;
  content: string;
  isFinal: boolean;
  toolCalls?: any[];
} 
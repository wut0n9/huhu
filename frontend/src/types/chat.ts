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
  url?: string; // 远程MCP工具的URL
  isRemote?: boolean; // 标识是否为远程工具
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
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  stream?: boolean;
  mcp_servers?: Array<{
    server_name: string;
    server_url: string;
  }>;
}

export interface ChatResponse {
  conversation_id: string;
  message: string;
  tool_calls?: any[];
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export interface StreamChatResponse {
  conversation_id: string;
  content: string;
  is_final: boolean;
  tool_calls?: any[];
}

export interface MCPServer {
  server_name: string;
  server_url: string;
}
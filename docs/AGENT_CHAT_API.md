# Agent Chat API 文档

## 概述

Agent Chat API 提供智能对话功能，支持工具调用、流式响应和MCP (Model Context Protocol) 服务器集成。该接口基于大语言模型，能够理解用户意图并调用相应的工具来完成任务。

## 接口信息

- **接口路径**: `POST /api/v1/agent/chat`
- **内容类型**: `application/json`
- **响应类型**: `text/event-stream` (流式) 或 `application/json` (非流式)

## 请求参数

### ChatRequest

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `message` | string | 是 | 用户消息内容 |
| `conversation_id` | string | 否 | 对话ID，用于维持对话上下文。如不提供将自动生成 |
| `stream` | boolean | 否 | 是否使用流式响应，默认为 `false` |
| `mcp_servers` | array | 否 | MCP服务器配置列表 |

### MCP服务器配置

每个MCP服务器配置包含以下字段：

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `server_name` | string | 是 | 服务器名称，用于标识服务器 |
| `server_url` | string | 是 | 服务器URL地址 |

## 响应格式

### 流式响应 (stream=true)

当 `stream=true` 时，接口返回 Server-Sent Events (SSE) 格式的流式响应：

```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
X-Accel-Buffering: no

data: {"conversation_id": "xxx", "content": "部分内容", "is_final": false, "tool_calls": null}

data: {"conversation_id": "xxx", "content": "更多内容", "is_final": false, "tool_calls": null}

data: {"conversation_id": "xxx", "content": "", "is_final": true, "tool_calls": null}
```

#### StreamChatResponse 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `conversation_id` | string | 对话ID |
| `content` | string | 响应内容片段 |
| `is_final` | boolean | 是否为最终响应 |
| `tool_calls` | array | 工具调用信息（如有） |

### 非流式响应 (stream=false)

当 `stream=false` 时，返回完整的JSON响应：

```json
{
  "conversation_id": "xxx",
  "message": "完整的响应内容",
  "tool_calls": null,
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_tokens": 150
  }
}
```

## 使用示例

### 基础对话示例

```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好，请介绍一下自己",
    "conversation_id": "demo-001",
    "stream": false
  }'
```

### 流式响应示例

```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "请详细解释什么是人工智能",
    "conversation_id": "demo-002",
    "stream": true
  }'
```

### 工具调用示例

```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "当前北京时间是几点了",
    "conversation_id": "demo-003",
    "stream": true,
    "mcp_servers": [
      {
        "server_name": "fetch",
        "server_url": "https://mcp.api-inference.modelscope.net/de4f7e6daf8d45/sse"
      },
      {
        "server_name": "time",
        "server_url": "https://mcp.api-inference.modelscope.net/e172de58a0434b/sse"
      }
    ]
  }'
```

### JavaScript 流式响应处理示例

```javascript
async function chatWithAgent(message, conversationId = null, mcpServers = []) {
  const response = await fetch('/api/v1/agent/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'text/event-stream'
    },
    body: JSON.stringify({
      message: message,
      conversation_id: conversationId,
      stream: true,
      mcp_servers: mcpServers
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6));
          console.log('收到响应:', data.content);
          
          if (data.is_final) {
            console.log('对话完成');
            return;
          }
        } catch (e) {
          console.error('解析响应失败:', e);
        }
      }
    }
  }
}

// 使用示例
chatWithAgent(
  "当前北京时间是几点了",
  "demo-004",
  [
    {
      "server_name": "time",
      "server_url": "https://mcp.api-inference.modelscope.net/e172de58a0434b/sse"
    }
  ]
);
```

## 错误处理

### HTTP 状态码

| 状态码 | 描述 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |

### 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

### 流式响应中的错误

在流式响应中，错误信息会作为最终响应发送：

```
data: {"conversation_id": "xxx", "content": "对话处理失败: 错误详情", "is_final": true}
```

## 功能特性

### 1. 智能对话
- 支持多轮对话，自动维护对话上下文
- 基于大语言模型的智能理解和回复

### 2. 工具调用
- 自动检测用户意图并调用相应工具
- 支持多轮工具调用
- 流式工具调用处理

### 3. MCP服务器集成
- 动态添加和管理MCP服务器
- 支持多个MCP服务器同时使用
- 自动工具发现和调用

### 4. 流式响应
- 实时内容输出，提升用户体验
- 支持Server-Sent Events (SSE)
- 可观察LLM思考过程

## 相关接口

### MCP服务器管理

- `POST /api/v1/agent/mcp/servers` - 添加MCP服务器
- `DELETE /api/v1/agent/mcp/servers/{server_name}` - 移除MCP服务器
- `GET /api/v1/agent/mcp/servers` - 列出所有MCP服务器
- `GET /api/v1/agent/mcp/tools` - 列出所有可用工具

### 对话管理

- `GET /api/v1/agent/conversations/{conversation_id}/history` - 获取对话历史
- `DELETE /api/v1/agent/conversations/{conversation_id}` - 清除对话历史

## 注意事项

1. **对话ID**: 建议为每个用户会话使用唯一的 `conversation_id` 来维持对话上下文
2. **MCP服务器**: 可以在请求中临时添加MCP服务器，也可以通过管理接口预先配置
3. **流式响应**: 使用流式响应时需要正确处理SSE格式的数据流
4. **错误处理**: 建议实现完善的错误处理机制，特别是在流式响应中
5. **超时设置**: 对于复杂的工具调用，建议设置合适的超时时间

## 版本信息

- API版本: v1
- 文档版本: 1.0
- 最后更新: 2025-08-03

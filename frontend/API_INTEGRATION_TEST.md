# API集成测试指南

## 概述

前端项目已经成功集成了后端的 `/api/v1/agent/chat` 接口。本文档说明如何测试API集成。

## 更新内容

### 1. 服务层更新 (`src/services/chat.ts`)
- ✅ 更新接口地址从 `/api/v1/chat` 到 `/api/v1/agent/chat`
- ✅ 实现流式响应处理
- ✅ 添加MCP服务器配置支持
- ✅ 改进错误处理

### 2. 类型定义更新 (`src/types/chat.ts`)
- ✅ 更新请求参数格式匹配API文档
- ✅ 更新响应数据结构
- ✅ 添加MCP服务器类型定义

### 3. Hook更新 (`src/hooks/useChat.ts`)
- ✅ 移除模拟数据逻辑
- ✅ 集成真实API调用
- ✅ 实现真正的流式响应处理
- ✅ 添加对话历史管理

## 测试方法

### 方法1：浏览器控制台测试

1. 打开浏览器访问 http://localhost:3001
2. 打开开发者工具控制台
3. 运行以下命令：

```javascript
// 测试所有API功能
testChatAPI.runAllTests()

// 或者单独测试
testChatAPI.testNonStreamingChat()  // 测试非流式响应
testChatAPI.testStreamingChat()     // 测试流式响应
testChatAPI.testMCPToolsChat()      // 测试MCP工具调用
```

### 方法2：UI界面测试

1. 确保后端服务运行在 http://localhost:8000
2. 在聊天界面输入消息
3. 观察流式响应效果
4. 测试MCP工具选择功能

## 前置条件

### 后端服务
确保后端服务正在运行：
```bash
# 检查后端服务状态
curl -X GET "http://localhost:8000/health"

# 如果没有运行，启动后端服务
# (具体启动命令根据后端项目而定)
```

### 环境变量
确保前端环境变量正确配置：
```bash
# frontend/.env.local 或 frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

## API接口映射

| 功能 | 前端方法 | 后端接口 |
|------|----------|----------|
| 发送消息(非流式) | `chatAPI.sendMessage()` | `POST /api/v1/agent/chat` |
| 发送消息(流式) | `chatAPI.sendMessageStream()` | `POST /api/v1/agent/chat` |
| 获取对话历史 | `chatAPI.getConversationHistory()` | `GET /api/v1/agent/conversations/{id}/history` |
| 清除对话 | `chatAPI.clearConversationHistory()` | `DELETE /api/v1/agent/conversations/{id}` |
| 获取MCP服务器 | `chatAPI.getMCPServers()` | `GET /api/v1/agent/mcp/servers` |
| 获取可用工具 | `chatAPI.getAvailableTools()` | `GET /api/v1/agent/mcp/tools` |

## 预期行为

### 流式响应
- 消息应该逐字符显示
- 显示速度约30ms/字符
- 完成后消息添加到历史记录

### 错误处理
- 网络错误显示友好提示
- API错误显示具体错误信息
- 流式响应中断时正确清理状态

### MCP工具集成
- 支持动态添加MCP服务器
- 工具调用结果正确显示
- 工具调用错误正确处理

## 故障排除

### 常见问题

1. **连接失败**
   - 检查后端服务是否运行
   - 检查端口号是否正确(8000)
   - 检查防火墙设置

2. **CORS错误**
   - 确保后端配置了正确的CORS设置
   - 检查请求头设置

3. **流式响应不工作**
   - 检查浏览器是否支持ReadableStream
   - 检查网络代理设置

4. **类型错误**
   - 检查TypeScript编译错误
   - 确保类型定义与API文档一致

## 下一步

- [ ] 添加单元测试
- [ ] 添加集成测试
- [ ] 优化错误处理
- [ ] 添加重试机制
- [ ] 实现离线支持

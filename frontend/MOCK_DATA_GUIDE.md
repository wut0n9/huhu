# Mock数据使用指南

## 概述

本项目已配置为使用mock数据，无需后端服务即可运行和测试所有功能。

## 功能特性

### ✅ 已实现的Mock功能

1. **用户认证**
   - 自动登录为"演示用户"
   - 用户信息：演示用户 (demo@example.com)
   - 无需登录验证，直接进入聊天页面

2. **聊天功能**
   - 模拟流式消息响应
   - 支持发送和接收消息
   - 自动生成对话历史

3. **对话管理**
   - 预设3个示例对话
   - 支持对话切换
   - 支持新建和清除对话

4. **文件上传**
   - 模拟文件上传过程
   - 显示上传进度
   - 支持文件管理

5. **MCP工具**
   - 预设5个示例工具
   - 支持工具选择和搜索
   - 工具配置管理

## 访问地址

- **聊天页面**: http://localhost:3000/chat
- **测试页面**: http://localhost:3000/test
- **首页**: http://localhost:3000 (自动跳转到聊天页面)

## Mock数据详情

### 用户数据
```typescript
{
  id: 1,
  username: 'demo_user',
  nickname: '演示用户',
  email: 'demo@example.com',
  role: 'user'
}
```

### 对话数据
- "关于项目开发的讨论" (15条消息)
- "技术问题咨询" (8条消息)  
- "API设计讨论" (12条消息)

### MCP工具
- file_system: 文件系统操作
- web_search: 网络搜索
- calculator: 计算器
- weather: 天气查询
- translator: 翻译工具

## 测试功能

### 1. 消息发送
- 在输入框输入消息
- 点击发送按钮或按Enter
- 观察模拟的流式响应

### 2. 文件上传
- 点击"上传文件"按钮
- 选择文件或拖拽上传
- 观察上传进度和结果

### 3. MCP工具
- 点击"MCP工具"按钮
- 搜索和选择工具
- 观察工具选择状态

### 4. 对话管理
- 点击左侧对话列表
- 测试对话切换功能
- 使用"新建"和"删除"功能

## 开发说明

### 修改Mock数据

1. **用户数据**: 修改 `src/hooks/useAuth.ts` 中的 `MOCK_USER`
2. **对话数据**: 修改 `src/hooks/useChat.ts` 中的 `MOCK_CONVERSATIONS`
3. **工具数据**: 修改 `src/components/ChatPage/MCPToolSelector.tsx` 中的 `MOCK_MCP_TOOLS`

### 添加新功能

1. 在相应的hook中添加mock逻辑
2. 模拟网络延迟和响应
3. 更新TypeScript类型定义

## 切换到真实API

当需要连接真实后端时：

1. 修改 `src/hooks/useAuth.ts` - 移除mock逻辑，使用真实API
2. 修改 `src/hooks/useChat.ts` - 移除mock逻辑，使用真实API
3. 修改 `src/components/ChatPage/MCPToolSelector.tsx` - 使用真实API获取工具列表
4. 确保后端服务运行在正确的端口

## 故障排除

### 开发服务器无法启动
```bash
# 检查Node.js版本
node --version  # 需要 18.x 或 20.x

# 重新安装依赖
rm -rf node_modules package-lock.json
npm install

# 启动开发服务器
npm run dev
```

### 页面显示异常
- 检查浏览器控制台错误
- 确认所有依赖已正确安装
- 清除浏览器缓存

### Mock数据不显示
- 检查浏览器控制台
- 确认mock数据已正确配置
- 检查组件是否正确导入

## 性能优化

- Mock数据已优化，模拟真实网络延迟
- 流式响应模拟真实体验
- 组件使用React.memo优化渲染性能 
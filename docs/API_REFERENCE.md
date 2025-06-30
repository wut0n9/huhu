# API参考文档

## 概述

本文档详细描述了大模型Agent应用平台的所有API接口，包括请求方法、参数、响应格式和示例。

## 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: JWT Bearer Token
- **数据格式**: JSON
- **字符编码**: UTF-8

## 认证

### 获取访问令牌

**POST** `/auth/login`

用户登录获取JWT访问令牌。

#### 请求参数
```json
{
  "username": "string",
  "password": "string"
}
```

#### 响应
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "string",
    "role": "string"
  }
}
```

#### 示例
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 用户注册

**POST** `/auth/register`

注册新用户账户。

#### 请求参数
```json
{
  "username": "string",
  "password": "string"
}
```

#### 响应
```json
{
  "id": 1,
  "username": "string",
  "role": "user"
}
```

## 用户管理

### 获取当前用户信息

**GET** `/users/me`

获取当前登录用户的详细信息。

#### 请求头
```
Authorization: Bearer <token>
```

#### 响应
```json
{
  "id": 1,
  "username": "string",
  "role": "string",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 获取用户列表

**GET** `/users/`

获取所有用户列表（需要管理员权限）。

#### 请求头
```
Authorization: Bearer <token>
```

#### 查询参数
- `page` (int, optional): 页码，默认1
- `size` (int, optional): 每页大小，默认10

#### 响应
```json
{
  "items": [
    {
      "id": 1,
      "username": "string",
      "role": "string",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 10
}
```

## 知识库管理

### 获取知识库列表

**GET** `/knowledge/`

获取所有知识库列表。

#### 请求头
```
Authorization: Bearer <token>
```

#### 查询参数
- `page` (int, optional): 页码，默认1
- `size` (int, optional): 每页大小，默认10
- `title` (string, optional): 按标题搜索

#### 响应
```json
{
  "items": [
    {
      "id": 1,
      "title": "string",
      "content": "string",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 10
}
```

### 创建知识库

**POST** `/knowledge/`

创建新的知识库。

#### 请求头
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

#### 请求参数
- `title` (string, required): 知识库标题
- `content` (string, optional): 文本内容
- `file` (file, optional): 上传文件

#### 响应
```json
{
  "id": 1,
  "title": "string",
  "content": "string",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 获取知识库详情

**GET** `/knowledge/{knowledge_id}`

获取指定知识库的详细信息。

#### 请求头
```
Authorization: Bearer <token>
```

#### 路径参数
- `knowledge_id` (int, required): 知识库ID

#### 响应
```json
{
  "id": 1,
  "title": "string",
  "content": "string",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "chunks": [
    {
      "id": 1,
      "chunk_index": 0,
      "content": "string",
      "vector_id": "string"
    }
  ]
}
```

### 删除知识库

**DELETE** `/knowledge/{knowledge_id}`

删除指定的知识库。

#### 请求头
```
Authorization: Bearer <token>
```

#### 路径参数
- `knowledge_id` (int, required): 知识库ID

#### 响应
```json
{
  "message": "Knowledge base deleted successfully"
}
```

## RAG问答

### 知识库问答

**POST** `/rag/query`

基于知识库进行智能问答。

#### 请求头
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### 请求参数
```json
{
  "knowledge_id": 1,
  "question": "string"
}
```

#### 响应
```json
{
  "answer": "string",
  "sources": [
    {
      "chunk_index": 0,
      "content": "string",
      "score": 0.95
    }
  ]
}
```

## MCP工具调用

### 获取MCP Server列表

**GET** `/mcp/servers`

获取可用的MCP Server列表。

#### 请求头
```
Authorization: Bearer <token>
```

#### 响应
```json
{
  "servers": [
    {
      "name": "string",
      "path": "string",
      "description": "string"
    }
  ]
}
```

### 获取工具列表

**GET** `/mcp/tools`

获取指定MCP Server的工具列表。

#### 请求头
```
Authorization: Bearer <token>
```

#### 查询参数
- `server_path` (string, required): MCP Server路径

#### 响应
```json
{
  "tools": [
    {
      "name": "string",
      "description": "string",
      "inputSchema": {
        "type": "object",
        "properties": {
          "param1": {
            "type": "string",
            "description": "string"
          }
        }
      }
    }
  ]
}
```

### 调用工具

**POST** `/mcp/call`

调用指定的MCP工具。

#### 请求头
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### 请求参数
```json
{
  "server_path": "string",
  "tool_name": "string",
  "arguments": {
    "param1": "value1"
  }
}
```

#### 响应
```json
{
  "result": "string",
  "error": null
}
```

## Text2SQL

### 自然语言转SQL

**POST** `/text2sql/convert`

将自然语言转换为SQL查询语句。

#### 请求头
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### 请求参数
```json
{
  "database_url": "string",
  "question": "string"
}
```

#### 响应
```json
{
  "sql": "SELECT * FROM table WHERE condition",
  "explanation": "string"
}
```

### 执行SQL查询

**POST** `/text2sql/execute`

执行SQL查询并返回结果。

#### 请求头
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### 请求参数
```json
{
  "database_url": "string",
  "sql": "string"
}
```

#### 响应
```json
{
  "columns": ["column1", "column2"],
  "data": [
    ["value1", "value2"],
    ["value3", "value4"]
  ],
  "row_count": 2
}
```

## ChatBI

### 开始对话

**POST** `/chatbi/chat`

开始ChatBI对话。

#### 请求头
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### 请求参数
```json
{
  "database_url": "string",
  "message": "string",
  "session_id": "string"
}
```

#### 响应
```json
{
  "response": "string",
  "sql": "SELECT * FROM table",
  "data": {
    "columns": ["column1"],
    "data": [["value1"]]
  },
  "chart": {
    "type": "bar",
    "options": {}
  },
  "session_id": "string"
}
```

## 数据可视化

### 生成图表

**POST** `/visualization/chart`

根据SQL查询结果生成图表。

#### 请求头
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### 请求参数
```json
{
  "database_url": "string",
  "sql": "string",
  "chart_type": "bar"
}
```

#### 响应
```json
{
  "data": {
    "columns": ["column1"],
    "data": [["value1"]]
  },
  "chart": {
    "type": "bar",
    "options": {
      "xAxis": {},
      "yAxis": {},
      "series": []
    }
  }
}
```

## 角色管理

### 获取角色列表

**GET** `/roles/`

获取所有角色列表。

#### 请求头
```
Authorization: Bearer <token>
```

#### 响应
```json
{
  "roles": [
    {
      "id": 1,
      "name": "string",
      "description": "string"
    }
  ]
}
```

### 创建角色

**POST** `/roles/`

创建新角色（需要管理员权限）。

#### 请求头
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### 请求参数
```json
{
  "name": "string",
  "description": "string"
}
```

#### 响应
```json
{
  "id": 1,
  "name": "string",
  "description": "string"
}
```

## 错误处理

### 错误响应格式

所有API错误都使用统一的响应格式：

```json
{
  "detail": "错误描述信息"
}
```

### 常见HTTP状态码

- `200 OK`: 请求成功
- `201 Created`: 资源创建成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未认证或认证失败
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在
- `422 Unprocessable Entity`: 请求数据验证失败
- `500 Internal Server Error`: 服务器内部错误

### 错误示例

#### 认证失败
```json
{
  "detail": "Could not validate credentials"
}
```

#### 参数验证失败
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 资源不存在
```json
{
  "detail": "Knowledge base not found"
}
```

## 速率限制

API接口实施速率限制以防止滥用：

- 认证接口：每分钟最多10次请求
- 其他接口：每分钟最多100次请求
- 超出限制返回429状态码

## 版本控制

API使用URL路径进行版本控制：

- 当前版本：`/api/v1/`
- 未来版本：`/api/v2/`

## 测试

### 使用curl测试

```bash
# 登录获取token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.access_token')

# 使用token访问API
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/users/me"
```

### 使用Swagger UI

访问 `http://localhost:8000/docs` 查看交互式API文档。

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持用户认证、知识库管理、RAG问答
- 支持MCP工具调用、Text2SQL、ChatBI
- 支持数据可视化功能 
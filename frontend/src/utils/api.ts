import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
export const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const { response } = error
    
    if (response) {
      switch (response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          ElMessage.error('登录已过期，请重新登录')
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(response.data?.detail || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

// API方法
export const authApi = {
  login: (data: any) => api.post('/auth/login', data),
  register: (data: any) => api.post('/auth/register', data),
  refresh: () => api.post('/auth/refresh'),
}

export const userApi = {
  getProfile: () => api.get('/users/me'),
  updateProfile: (data: any) => api.put('/users/me', data),
}

export const agentApi = {
  getAgents: (params?: any) => api.get('/agents', { params }),
  getAgent: (id: number) => api.get(`/agents/${id}`),
  createAgent: (data: any) => api.post('/agents', data),
  updateAgent: (id: number, data: any) => api.put(`/agents/${id}`, data),
  updateAgentStatus: (id: number, status: any) => api.patch(`/agents/${id}/status`, status),
  deleteAgent: (id: number) => api.delete(`/agents/${id}`),
}

export const conversationApi = {
  getConversations: (params?: any) => api.get('/conversations', { params }),
  getConversation: (id: number) => api.get(`/conversations/${id}`),
  createConversation: (data: any) => api.post('/conversations', data),
  updateConversation: (id: number, data: any) => api.put(`/conversations/${id}`, data),
  deleteConversation: (id: number) => api.delete(`/conversations/${id}`),
  chat: (data: any) => api.post('/conversations/chat', data),
} 
import { request } from './api';
import { LoginRequest, LoginResponse, RegisterRequest, User } from '@/types/user';

// 认证相关API
export const authAPI = {
  // 用户登录
  login: (data: LoginRequest): Promise<LoginResponse> => {
    return request.post('/auth/login', data);
  },

  // 用户注册
  register: (data: RegisterRequest): Promise<{ user: User }> => {
    return request.post('/auth/register', data);
  },

  // 获取当前用户信息
  getCurrentUser: (): Promise<{ user: User }> => {
    return request.get('/auth/me');
  },

  // 用户登出
  logout: (): Promise<{ message: string }> => {
    return request.post('/auth/logout');
  },

  // 刷新token
  refreshToken: (): Promise<{ access_token: string; token_type: string }> => {
    return request.post('/auth/refresh');
  },
}; 
import { useState, useCallback, useEffect } from 'react';
import { User } from '@/types/user';

// Mock用户数据
const MOCK_USER: User = {
  id: 1,
  username: 'demo_user',
  nickname: '演示用户',
  email: 'demo@example.com',
  avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=demo',
  role: 'user',
  isActive: true,
  createdAt: '2024-01-01T00:00:00Z',
  updatedAt: '2024-01-01T00:00:00Z'
};

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const useAuth = () => {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true
  });

  // 模拟登录
  const login = useCallback(async () => {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    setState({
      user: MOCK_USER,
      isAuthenticated: true,
      isLoading: false
    });
    
    return { success: true, user: MOCK_USER };
  }, []);

  // 模拟注册
  const register = useCallback(async () => {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    setState({
      user: MOCK_USER,
      isAuthenticated: true,
      isLoading: false
    });
    
    return { success: true, user: MOCK_USER };
  }, []);

  // 模拟登出
  const logout = useCallback(async () => {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 500));
    
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false
    });
    
    return { success: true };
  }, []);

  // 模拟检查认证状态
  const checkAuth = useCallback(async () => {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // 直接设置为已登录状态
    setState({
      user: MOCK_USER,
      isAuthenticated: true,
      isLoading: false
    });
    
    return { success: true, user: MOCK_USER };
  }, []);

  // 组件挂载时检查认证状态
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return {
    ...state,
    login,
    register,
    logout,
    checkAuth
  };
};

export default useAuth; 
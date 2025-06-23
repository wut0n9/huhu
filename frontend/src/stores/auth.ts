import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/utils/api'
import type { User, UserLogin, UserCreate } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(credentials: UserLogin) {
    try {
      const response = await api.post('/auth/login', credentials)
      const { access_token } = response.data
      
      token.value = access_token
      localStorage.setItem('token', access_token)
      
      // 获取用户信息
      await fetchUser()
      
      return { success: true }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data?.detail || '登录失败' 
      }
    }
  }

  async function register(userData: UserCreate) {
    try {
      const response = await api.post('/auth/register', userData)
      return { success: true, data: response.data }
    } catch (error: any) {
      return { 
        success: false, 
        error: error.response?.data?.detail || '注册失败' 
      }
    }
  }

  async function fetchUser() {
    try {
      const response = await api.get('/users/me')
      user.value = response.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  // 初始化时获取用户信息
  if (token.value) {
    fetchUser()
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
}) 
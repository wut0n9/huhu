<template>
  <div class="home-container">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="250px" class="sidebar">
        <div class="sidebar-header">
          <h2>Agent平台</h2>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          router
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          
          <el-menu-item index="/agents">
            <el-icon><Robot /></el-icon>
            <span>Agent管理</span>
          </el-menu-item>
          
          <el-menu-item index="/conversations">
            <el-icon><ChatDotRound /></el-icon>
            <span>对话历史</span>
          </el-menu-item>
          
          <el-menu-item index="/profile">
            <el-icon><User /></el-icon>
            <span>个人设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header class="header">
          <div class="header-left">
            <h3>欢迎回来，{{ user?.full_name || user?.username }}</h3>
          </div>
          
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                <el-avatar :size="32" :src="user?.avatar_url">
                  {{ user?.username?.charAt(0).toUpperCase() }}
                </el-avatar>
                <span class="username">{{ user?.username }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人设置</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- 内容区 -->
        <el-main class="main-content">
          <div class="dashboard">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon">
                      <el-icon size="32"><Robot /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.agents }}</div>
                      <div class="stat-label">我的Agent</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <el-col :span="8">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon">
                      <el-icon size="32"><ChatDotRound /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.conversations }}</div>
                      <div class="stat-label">对话总数</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <el-col :span="8">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon">
                      <el-icon size="32"><DataAnalysis /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.tokens }}</div>
                      <div class="stat-label">Token使用量</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            
            <el-row :gutter="20" style="margin-top: 20px;">
              <el-col :span="12">
                <el-card>
                  <template #header>
                    <div class="card-header">
                      <span>快速开始</span>
                    </div>
                  </template>
                  
                  <div class="quick-actions">
                    <el-button type="primary" @click="createAgent">
                      <el-icon><Plus /></el-icon>
                      创建新Agent
                    </el-button>
                    
                    <el-button @click="startChat">
                      <el-icon><ChatDotRound /></el-icon>
                      开始对话
                    </el-button>
                  </div>
                </el-card>
              </el-col>
              
              <el-col :span="12">
                <el-card>
                  <template #header>
                    <div class="card-header">
                      <span>最近对话</span>
                    </div>
                  </template>
                  
                  <div v-if="recentConversations.length === 0" class="empty-state">
                    <el-icon size="48" color="#ccc"><ChatDotRound /></el-icon>
                    <p>暂无对话记录</p>
                  </div>
                  
                  <div v-else class="conversation-list">
                    <div
                      v-for="conversation in recentConversations"
                      :key="conversation.id"
                      class="conversation-item"
                      @click="openConversation(conversation.id)"
                    >
                      <div class="conversation-title">{{ conversation.title || '无标题对话' }}</div>
                      <div class="conversation-meta">
                        {{ formatDate(conversation.created_at) }}
                      </div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { conversationApi } from '@/utils/api'
import type { Conversation } from '@/types'
import dayjs from 'dayjs'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const activeMenu = computed(() => route.path)

const stats = ref({
  agents: 0,
  conversations: 0,
  tokens: 0
})

const recentConversations = ref<Conversation[]>([])

onMounted(async () => {
  await loadStats()
  await loadRecentConversations()
})

const loadStats = async () => {
  try {
    // 这里应该调用实际的API获取统计数据
    stats.value = {
      agents: 5,
      conversations: 23,
      tokens: 15420
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadRecentConversations = async () => {
  try {
    const response = await conversationApi.getConversations({ limit: 5 })
    recentConversations.value = response.data
  } catch (error) {
    console.error('加载最近对话失败:', error)
  }
}

const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'logout':
      authStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
      break
  }
}

const createAgent = () => {
  router.push('/agents')
}

const startChat = () => {
  router.push('/chat')
}

const openConversation = (id: number) => {
  router.push(`/chat?conversation=${id}`)
}

const formatDate = (date: string) => {
  return dayjs(date).format('MM-DD HH:mm')
}
</script>

<style scoped>
.home-container {
  height: 100vh;
}

.sidebar {
  background: #304156;
  color: white;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #435266;
}

.sidebar-header h2 {
  margin: 0;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.sidebar-menu {
  border: none;
  background: transparent;
}

.header {
  background: white;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left h3 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 500;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.username {
  margin: 0 8px;
  color: #333;
  font-size: 14px;
}

.main-content {
  background: #f5f7fa;
  padding: 20px;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  height: 120px;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  margin-right: 16px;
  color: #409eff;
}

.stat-number {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  line-height: 1;
}

.stat-label {
  margin-top: 4px;
  color: #666;
  font-size: 14px;
}

.card-header {
  font-weight: 600;
  color: #333;
}

.quick-actions {
  display: flex;
  gap: 12px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-state p {
  margin: 12px 0 0 0;
  font-size: 14px;
}

.conversation-list {
  max-height: 300px;
  overflow-y: auto;
}

.conversation-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.conversation-item:hover {
  background-color: #f5f7fa;
}

.conversation-item:last-child {
  border-bottom: none;
}

.conversation-title {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-meta {
  font-size: 12px;
  color: #999;
}
</style> 
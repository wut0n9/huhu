<template>
  <div class="agents-container">
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
            <h3>Agent管理</h3>
          </div>
          
          <div class="header-right">
            <el-button type="primary" @click="showCreateDialog = true">
              <el-icon><Plus /></el-icon>
              创建Agent
            </el-button>
          </div>
        </el-header>
        
        <!-- 内容区 -->
        <el-main class="main-content">
          <div class="agents-content">
            <!-- 搜索和筛选 -->
            <div class="search-bar">
              <el-input
                v-model="searchQuery"
                placeholder="搜索Agent..."
                prefix-icon="Search"
                clearable
                @input="handleSearch"
              />
              
              <el-select v-model="statusFilter" placeholder="状态筛选" clearable>
                <el-option label="全部" value="" />
                <el-option label="空闲" value="idle" />
                <el-option label="运行中" value="running" />
                <el-option label="暂停" value="paused" />
                <el-option label="错误" value="error" />
                <el-option label="已停止" value="stopped" />
              </el-select>
            </div>
            
            <!-- Agent列表 -->
            <div class="agents-grid">
              <el-card
                v-for="agent in filteredAgents"
                :key="agent.id"
                class="agent-card"
                shadow="hover"
              >
                <div class="agent-header">
                  <div class="agent-title">
                    <h4>{{ agent.name }}</h4>
                    <el-tag :type="getStatusType(agent.status)" size="small">
                      {{ getStatusText(agent.status) }}
                    </el-tag>
                  </div>
                  
                  <el-dropdown @command="handleAgentCommand">
                    <el-button type="text" size="small">
                      <el-icon><MoreFilled /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item :command="{ action: 'edit', agent }">
                          编辑
                        </el-dropdown-item>
                        <el-dropdown-item :command="{ action: 'chat', agent }">
                          开始对话
                        </el-dropdown-item>
                        <el-dropdown-item :command="{ action: 'delete', agent }" divided>
                          删除
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
                
                <div class="agent-description">
                  {{ agent.description || '暂无描述' }}
                </div>
                
                <div class="agent-stats">
                  <div class="stat-item">
                    <span class="stat-label">对话数:</span>
                    <span class="stat-value">{{ agent.total_conversations }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Token:</span>
                    <span class="stat-value">{{ agent.total_tokens_used }}</span>
                  </div>
                </div>
                
                <div class="agent-actions">
                  <el-button type="primary" size="small" @click="startChat(agent)">
                    开始对话
                  </el-button>
                  <el-button size="small" @click="editAgent(agent)">
                    编辑
                  </el-button>
                </div>
              </el-card>
            </div>
            
            <!-- 空状态 -->
            <div v-if="filteredAgents.length === 0" class="empty-state">
              <el-icon size="64" color="#ccc"><Robot /></el-icon>
              <h3>暂无Agent</h3>
              <p>创建您的第一个Agent开始使用</p>
              <el-button type="primary" @click="showCreateDialog = true">
                创建Agent
              </el-button>
            </div>
          </div>
        </el-main>
      </el-container>
    </el-container>
    
    <!-- 创建Agent对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="创建新Agent"
      width="600px"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="createForm.name" placeholder="请输入Agent名称" />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="createForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入Agent描述"
          />
        </el-form-item>
        
        <el-form-item label="类型" prop="agent_type">
          <el-select v-model="createForm.agent_type" placeholder="选择Agent类型">
            <el-option label="聊天" value="chat" />
            <el-option label="任务" value="task" />
            <el-option label="工作流" value="workflow" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="系统提示词" prop="system_prompt">
          <el-input
            v-model="createForm.system_prompt"
            type="textarea"
            :rows="4"
            placeholder="请输入系统提示词"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" :loading="creating" @click="handleCreate">
          创建
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { agentApi } from '@/utils/api'
import type { Agent, AgentCreate } from '@/types'

const router = useRouter()
const route = useRoute()

const activeMenu = computed(() => route.path)

const agents = ref<Agent[]>([])
const searchQuery = ref('')
const statusFilter = ref('')
const showCreateDialog = ref(false)
const creating = ref(false)

const createFormRef = ref<FormInstance>()
const createForm = ref<AgentCreate>({
  name: '',
  description: '',
  agent_type: 'chat',
  system_prompt: '',
  model_config: {
    model_name: 'gpt-3.5-turbo',
    temperature: 0.7,
    max_tokens: 1000
  }
})

const createRules: FormRules = {
  name: [
    { required: true, message: '请输入Agent名称', trigger: 'blur' },
    { min: 1, max: 100, message: '名称长度在 1 到 100 个字符', trigger: 'blur' }
  ],
  agent_type: [
    { required: true, message: '请选择Agent类型', trigger: 'change' }
  ]
}

const filteredAgents = computed(() => {
  let filtered = agents.value
  
  if (searchQuery.value) {
    filtered = filtered.filter(agent =>
      agent.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      agent.description?.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  if (statusFilter.value) {
    filtered = filtered.filter(agent => agent.status === statusFilter.value)
  }
  
  return filtered
})

onMounted(() => {
  loadAgents()
})

const loadAgents = async () => {
  try {
    const response = await agentApi.getAgents()
    agents.value = response.data
  } catch (error) {
    console.error('加载Agent列表失败:', error)
    ElMessage.error('加载Agent列表失败')
  }
}

const handleSearch = () => {
  // 搜索逻辑已在computed中处理
}

const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    idle: 'info',
    running: 'success',
    paused: 'warning',
    error: 'danger',
    stopped: ''
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    idle: '空闲',
    running: '运行中',
    paused: '暂停',
    error: '错误',
    stopped: '已停止'
  }
  return statusMap[status] || status
}

const handleAgentCommand = (command: any) => {
  switch (command.action) {
    case 'edit':
      editAgent(command.agent)
      break
    case 'chat':
      startChat(command.agent)
      break
    case 'delete':
      deleteAgent(command.agent)
      break
  }
}

const editAgent = (agent: Agent) => {
  router.push(`/agents/${agent.id}/edit`)
}

const startChat = (agent: Agent) => {
  router.push(`/chat/${agent.id}`)
}

const deleteAgent = async (agent: Agent) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除Agent "${agent.name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await agentApi.deleteAgent(agent.id)
    ElMessage.success('删除成功')
    await loadAgents()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除Agent失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleCreate = async () => {
  if (!createFormRef.value) return
  
  try {
    await createFormRef.value.validate()
    creating.value = true
    
    await agentApi.createAgent(createForm.value)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    
    // 重置表单
    createForm.value = {
      name: '',
      description: '',
      agent_type: 'chat',
      system_prompt: '',
      model_config: {
        model_name: 'gpt-3.5-turbo',
        temperature: 0.7,
        max_tokens: 1000
      }
    }
    
    await loadAgents()
  } catch (error) {
    console.error('创建Agent失败:', error)
    ElMessage.error('创建失败')
  } finally {
    creating.value = false
  }
}
</script>

<style scoped>
.agents-container {
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

.main-content {
  background: #f5f7fa;
  padding: 20px;
}

.agents-content {
  max-width: 1200px;
  margin: 0 auto;
}

.search-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.search-bar .el-input {
  width: 300px;
}

.search-bar .el-select {
  width: 150px;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.agent-card {
  transition: transform 0.2s;
}

.agent-card:hover {
  transform: translateY(-2px);
}

.agent-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.agent-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.agent-title h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.agent-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
  line-height: 1.5;
}

.agent-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.agent-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #999;
}

.empty-state h3 {
  margin: 16px 0 8px 0;
  color: #666;
  font-size: 18px;
}

.empty-state p {
  margin: 0 0 24px 0;
  font-size: 14px;
}
</style> 
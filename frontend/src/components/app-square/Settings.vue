<template>
  <div class="agent-detail agent-detail-enter">
    <div class="agent-detail-card">
      <div class="agent-detail-header">
        <h2 class="agent-detail-title">空间天气问答系统设置</h2>
        <div class="agent-detail-actions">
          <button 
            class="action-icon-btn"
            title="关闭"
            @click="handleCancel"
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
      
      <div class="settings-content">
        <!-- 系统名称 -->
        <div class="form-section">
          <label class="form-label">系统名称</label>
          <input
            v-model="agentName"
            type="text"
            class="form-input"
            placeholder="请输入系统名称"
          />
        </div>

        <!-- 系统简介 -->
        <div class="form-section">
          <label class="form-label">系统简介</label>
          <textarea
            v-model="agentDescription"
            class="form-textarea"
            placeholder="请输入系统简介"
            rows="4"
          ></textarea>
        </div>

        <!-- 文档管理 -->
        <div class="form-section">
          <label class="form-label">相关文档</label>
          
          <!-- 文档列表 -->
          <div v-if="documents.length > 0" class="documents-list">
            <div
              v-for="(doc, index) in documents"
              :key="index"
              class="document-item"
            >
              <div class="document-info">
                <svg class="document-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <div class="document-details">
                  <span class="document-name">{{ doc.name }}</span>
                  <span class="document-size">{{ formatFileSize(doc.size) }}</span>
                </div>
              </div>
              <button
                class="document-delete-btn"
                title="删除"
                @click="deleteDocument(index)"
              >
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- 上传区域 -->
          <div
            class="upload-area"
            @click="triggerFileInput"
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <input
              ref="fileInput"
              type="file"
              multiple
              accept=".pdf,.doc,.docx,.xls,.xlsx,.txt"
              @change="handleFileSelect"
              style="display: none"
            />
            <svg class="upload-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M17 8L12 3L7 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <p class="upload-text">点击或拖拽文件到此处上传</p>
            <p class="upload-hint">支持PDF、Word、Excel、TXT格式，上传空间天气相关文档后将自动训练向量数据库</p>
          </div>
        </div>
      </div>
      
      <!-- 底部操作按钮 -->
      <div class="settings-footer">
        <button class="btn btn-cancel" @click="handleCancel">取消</button>
        <button class="btn btn-apply" @click="handleApply">应用</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  agent: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'update'])

const agentName = ref('')
const agentDescription = ref('')
const documents = ref([])
const fileInput = ref(null)

// 原始数据备份（用于取消时恢复）
const originalName = ref('')
const originalDescription = ref('')
const originalDocuments = ref([])

// 初始化数据函数
const initializeData = () => {
  if (props.agent) {
    agentName.value = props.agent.name || ''
    agentDescription.value = props.agent.description || ''
    documents.value = props.agent.documents || []
    
    // 保存原始数据
    originalName.value = props.agent.name || ''
    originalDescription.value = props.agent.description || ''
    originalDocuments.value = props.agent.documents ? [...props.agent.documents] : []
  } else {
    agentName.value = ''
    agentDescription.value = ''
    documents.value = []
    originalName.value = ''
    originalDescription.value = ''
    originalDocuments.value = []
  }
}

// 加载文档列表
const loadDocuments = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/documents/default')
    if (response.ok) {
      const data = await response.json()
      if (data.documents && Array.isArray(data.documents)) {
        documents.value = data.documents.map(doc => ({
          id: doc.id || doc.file_id,
          name: doc.filename || doc.name,
          size: doc.size || 0,
          type: doc.type || '',
          uploading: false
        }))
        originalDocuments.value = [...documents.value]
      }
    }
  } catch (error) {
    console.error('加载文档列表错误:', error)
  }
}

// 初始化数据
onMounted(() => {
  initializeData()
  loadDocuments()
})

// 监听agent变化
watch(() => props.agent, () => {
  initializeData()
}, { immediate: true, deep: true })

// 应用设置
const handleApply = () => {
  emit('update', {
    name: agentName.value,
    description: agentDescription.value,
    documents: documents.value
  })
  // 更新原始数据
  originalName.value = agentName.value
  originalDescription.value = agentDescription.value
  originalDocuments.value = [...documents.value]
  // 关闭设置窗口
  emit('close')
}

// 取消设置
const handleCancel = () => {
  // 恢复原始数据
  agentName.value = originalName.value
  agentDescription.value = originalDescription.value
  documents.value = [...originalDocuments.value]
  // 关闭设置窗口
  emit('close')
}

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileSelect = async (event) => {
  const files = event.target.files
  if (files.length === 0) return
  
  for (const file of files) {
    await uploadFile(file)
  }
  
  event.target.value = ''
}

// 处理拖拽
const handleDrop = async (event) => {
  event.preventDefault()
  const files = event.dataTransfer.files
  if (files.length === 0) return
  
  for (const file of files) {
    await uploadFile(file)
  }
}

// 上传文件
const uploadFile = async (file) => {
  // 检查文件类型
  const allowedTypes = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt']
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
  if (!allowedTypes.includes(fileExtension)) {
    alert('不支持的文件类型，请上传PDF、Word、Excel或TXT格式的文件')
    return
  }

  // 添加到文档列表（先显示，后上传）
  const document = {
    name: file.name,
    size: file.size,
    type: file.type,
    file: file,
    uploading: true
  }
  documents.value.push(document)

  // 上传到服务器
  const formData = new FormData()
  formData.append('file', file)
  formData.append('company_id', 'default')
  
  try {
    const response = await fetch('http://localhost:8000/api/upload', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('上传失败')
    }
    
    const data = await response.json()
    console.log('文件上传成功:', data)
    
    // 更新文档状态
    document.uploading = false
    document.id = data.id || data.file_id
    document.url = data.url || data.file_url
  } catch (error) {
    console.error('上传文件错误:', error)
    // 从列表中移除
    const index = documents.value.indexOf(document)
    if (index > -1) {
      documents.value.splice(index, 1)
    }
    alert('文件上传失败，请重试')
  }
}

// 删除文档
const deleteDocument = async (index) => {
  if (!confirm('确定要删除这个文档吗？')) {
    return
  }
  
  const document = documents.value[index]
  if (document && document.id) {
    try {
      const response = await fetch(`http://localhost:8000/api/documents/default/${document.id}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error('删除失败')
      }
      
      documents.value.splice(index, 1)
    } catch (error) {
      console.error('删除文档错误:', error)
      alert('删除文档失败，请重试')
    }
  } else {
    // 如果没有id，直接从前端列表中移除
    documents.value.splice(index, 1)
  }
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}
</script>

<style scoped>
.agent-detail {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 0;
  gap: 0;
  overflow: hidden;
  justify-content: flex-start;
  height: 100vh;
  width: 100%;
}

.agent-detail-enter {
  animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes slideInRight {
  0% {
    opacity: 0;
    transform: translateX(30px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

.agent-detail-card {
  background: transparent;
  backdrop-filter: none;
  border: none;
  border-radius: 0;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 100vh;
  height: 100vh;
  overflow: hidden;
  box-shadow: none;
  width: 100%;
}

.agent-detail-header {
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: transparent;
}

.agent-detail-title {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0;
}

.agent-detail-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-icon-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: var(--text-primary);
}

.action-icon-btn svg {
  width: 18px;
  height: 18px;
}

.settings-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  padding-bottom: 3rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  color: var(--text-primary);
  font-size: 0.875rem;
  font-family: inherit;
  outline: none;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-textarea:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(59, 130, 246, 0.5);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.document-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.document-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.document-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.document-icon {
  width: 20px;
  height: 20px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.document-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
  min-width: 0;
}

.document-name {
  font-size: 0.875rem;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-size {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.document-delete-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: transparent;
  border: none;
  border-radius: 0.375rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
  flex-shrink: 0;
}

.document-delete-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: rgb(239, 68, 68);
}

.document-delete-btn svg {
  width: 16px;
  height: 16px;
}

.upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 0.75rem;
  padding: 2.5rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.02);
}

.upload-area:hover {
  border-color: rgba(59, 130, 246, 0.5);
  background: rgba(59, 130, 246, 0.05);
}

.upload-icon {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  color: var(--text-secondary);
}

.upload-text {
  color: var(--text-primary);
  font-size: 0.9375rem;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.upload-hint {
  color: var(--text-secondary);
  font-size: 0.8125rem;
  margin: 0;
}

.settings-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  background: transparent;
  flex-shrink: 0;
}

.btn {
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  outline: none;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-secondary);
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: var(--text-primary);
}

.btn-apply {
  background: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: rgb(59, 130, 246);
}

.btn-apply:hover {
  background: rgba(59, 130, 246, 0.3);
  border-color: rgba(59, 130, 246, 0.5);
  color: rgb(96, 165, 250);
}
</style>


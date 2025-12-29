<template>
  <div class="app-square-container">
    <!-- Black Hole Background -->
    <BlackHoleBackground />
    
    <!-- Main Content -->
    <main class="main-content">
      <div class="content-layout">
        <!-- Q&A Agent 对话框区域 -->
        <section class="content-area">
          <!-- 对话框区域 -->
          <ChatDialog
            v-if="!showSettings"
            agent-name="空间天气问答系统"
            :messages="messages"
            :is-loading="isLoading"
            :show-settings-button="true"
            :messages-container-ref="messagesContainer"
            @open-settings="showSettings = true"
            @retry="handleRetry"
            @copy="handleCopy"
            @share="handleShare"
            @like="handleLike"
            @dislike="handleDislike"
            @edit="handleEdit"
            @resend="handleResend"
          />
          
          <!-- 设置窗口 -->
          <Settings
            v-else-if="showSettings"
            :agent="qaAgent"
            @close="showSettings = false"
            @update="handleSettingsUpdate"
          />

          <!-- 输入框区域（固定在底部） -->
          <InputBox
            v-if="!showSettings"
            v-model="currentQuestion"
            placeholder="请输入关于空间天气的问题..."
            :is-fixed="true"
            :show-title="false"
            :show-description="false"
            :show-examples="false"
            :disabled="!currentQuestion.trim() || isLoading"
            @submit="sendQuestion"
          />
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import BlackHoleBackground from '../components/BlackHoleBackground.vue'
import ChatDialog from '../components/app-square/ChatDialog.vue'
import InputBox from '../components/app-square/InputBox.vue'
import Settings from '../components/app-square/Settings.vue'
import { useChat } from '../composables/useChat'

// Q&A Agent配置
const qaAgent = ref({
  id: 1,
  name: '空间天气问答系统',
  description: '专业的空间天气知识问答系统，基于RAG技术提供准确的空间天气信息',
  documents: []
})

// 设置窗口状态
const showSettings = ref(false)

// 使用chat composable
const messagesContainer = ref(null)
const { messages, currentQuestion, isLoading, sendQuestion: sendChatQuestion, clearMessages, addWelcomeMessage } = useChat(messagesContainer)

// 组件挂载时显示欢迎消息
onMounted(() => {
  nextTick(() => {
    addWelcomeMessage('空间天气问答系统')
  })
})

// 发送问题
const sendQuestion = async () => {
  await sendChatQuestion()
}

// 处理消息操作
const handleRetry = (messageIndex) => {
  // 找到对应的用户消息（通常是前一条）
  if (messageIndex > 0 && messages.value[messageIndex - 1]?.type === 'user') {
    const userQuestion = messages.value[messageIndex - 1].content
    // 删除当前助手消息及之后的所有消息
    messages.value = messages.value.slice(0, messageIndex - 1)
    // 重新发送问题
    currentQuestion.value = userQuestion
    nextTick(() => {
      sendQuestion()
    })
  }
}

const handleCopy = (content) => {
  navigator.clipboard.writeText(content).then(() => {
    console.log('已复制到剪贴板')
  }).catch(err => {
    console.error('复制失败:', err)
  })
}

const handleShare = (content) => {
  if (navigator.share) {
    navigator.share({
      title: '空间天气问答系统回答',
      text: content
    }).catch(err => {
      console.error('分享失败:', err)
    })
  } else {
    handleCopy(content)
  }
}

const handleLike = (messageIndex) => {
  if (messages.value[messageIndex]) {
    const message = messages.value[messageIndex]
    if (message.liked) {
      message.liked = false
    } else {
      message.liked = true
      message.disliked = false
    }
  }
}

const handleDislike = (messageIndex) => {
  if (messages.value[messageIndex]) {
    const message = messages.value[messageIndex]
    if (message.disliked) {
      message.disliked = false
    } else {
      message.disliked = true
      message.liked = false
    }
  }
}

const handleEdit = (messageIndex, newContent) => {
  if (messages.value[messageIndex] && messages.value[messageIndex].type === 'user') {
    messages.value[messageIndex].content = newContent
    messages.value[messageIndex].isEditing = false
  }
}

const handleSettingsUpdate = (settings) => {
  qaAgent.value.name = settings.name
  qaAgent.value.description = settings.description
  qaAgent.value.documents = settings.documents
  // TODO: 调用API保存设置
  console.log('更新Agent设置:', settings)
}

const handleResend = async (messageIndex, newContent) => {
  if (messages.value[messageIndex] && messages.value[messageIndex].type === 'user') {
    // 更新消息内容
    messages.value[messageIndex].content = newContent
    messages.value[messageIndex].isEditing = false
    
    // 删除该消息之后的所有消息（包括助手回复）
    messages.value = messages.value.slice(0, messageIndex + 1)
    
    // 重新发送问题
    currentQuestion.value = newContent
    await nextTick()
    await sendQuestion()
  }
}
</script>

<style scoped>
.app-square-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  background: transparent;
  overflow-x: hidden;
}

.main-content {
  flex: 1;
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-layout {
  display: flex;
  flex: 1;
  min-height: 100vh;
  justify-content: center;
  align-items: center;
}

.content-area {
  flex: 1;
  width: 100%;
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  position: relative;
  overflow: hidden;
  height: 100vh;
}
</style>

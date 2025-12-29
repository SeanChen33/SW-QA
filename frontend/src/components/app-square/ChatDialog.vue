<template>
  <div class="agent-detail agent-detail-enter">
    <div class="agent-detail-card">
      <div class="agent-detail-header">
        <h2 class="agent-detail-title">{{ agentName }}</h2>
        <div class="agent-detail-actions">
          <button 
            v-if="showSettingsButton" 
            class="action-icon-btn"
            title="设置"
            @click="$emit('open-settings')"
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M19.6226 10.3954L18.5247 7.7448L20 6L18 4L16.2647 5.4829L13.5577 4.3698L12.9353 2H11.0647L10.4423 4.3698L7.73529 5.4829L6 4L4 6L5.47529 7.7448L4.37741 10.3954L2 11.2361V12.7639L4.37741 13.6046L5.47529 16.2552L4 18L6 20L7.73529 18.5171L10.4423 19.6302L11.0647 22H12.9353L13.5577 19.6302L16.2647 18.5171L18 20L20 18L18.5247 16.2552L19.6226 13.6046L22 12.7639V11.2361L19.6226 10.3954Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
      
      <div class="messages-container" ref="messagesContainerRef">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.type]"
        >
          <template v-if="message.type === 'user'">
            <div class="user-message-container">
              <div class="message-content user-message">
                <div v-if="!message.isEditing" class="message-text">{{ message.content }}</div>
                <textarea
                  v-else
                  v-model="editingText"
                  class="message-edit-input"
                  @keydown.esc="cancelEdit(index)"
                  autofocus
                ></textarea>
              </div>
              <div v-if="!message.isEditing" class="message-actions user-message-actions">
                <button 
                  class="message-action-btn" 
                  title="编辑"
                  @click="editMessage(index)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M18.5 2.50023C18.8978 2.10243 19.4374 1.87891 20 1.87891C20.5626 1.87891 21.1022 2.10243 21.5 2.50023C21.8978 2.89804 22.1213 3.43762 22.1213 4.00023C22.1213 4.56284 21.8978 5.10243 21.5 5.50023L12 15.0002L8 16.0002L9 12.0002L18.5 2.50023Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button 
                  class="message-action-btn" 
                  title="复制"
                  @click="copyMessage(message.content)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M5 15H4C2.89543 15 2 14.1046 2 13V4C2 2.89543 2.89543 2 4 2H13C14.1046 2 15 2.89543 15 4V5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button 
                  class="message-action-btn" 
                  title="分享"
                  @click="shareMessage(message.content)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 8C19.6569 8 21 6.65685 21 5C21 3.34315 19.6569 2 18 2C16.3431 2 15 3.34315 15 5C15 5.27368 15.0522 5.53588 15.1496 5.77804L8.85041 9.22196C8.44784 8.45813 7.65685 8 6.75 8C5.23122 8 4 9.23122 4 10.75C4 12.2688 5.23122 13.5 6.75 13.5C7.65685 13.5 8.44784 13.0419 8.85041 12.278L15.1496 15.722C15.0522 15.9641 15 16.2263 15 16.5C15 18.1569 16.3431 19.5 18 19.5C19.6569 19.5 21 18.1569 21 16.5C21 14.8431 19.6569 13.5 18 13.5C17.0932 13.5 16.3022 13.9581 15.8996 14.722L9.60041 11.278C9.69797 11.0359 9.75 10.7737 9.75 10.5C9.75 10.2263 9.69797 9.96412 9.60041 9.72196L15.8996 6.27804C16.3022 7.04187 17.0932 7.5 18 7.5V8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
              <div v-else class="message-actions user-message-actions edit-actions">
                <button 
                  class="message-action-btn edit-btn" 
                  title="重新发送"
                  @click="resendMessage(index)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button 
                  class="message-action-btn cancel-btn" 
                  title="取消"
                  @click="cancelEdit(index)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="message-content">
              <div class="message-wrapper">
                <div class="message-text markdown-content" v-html="formatMessage(message.content)"></div>
                <div v-if="!message.isStreaming" class="message-actions">
                <button 
                  class="message-action-btn" 
                  title="复制"
                  @click="copyMessage(message.content)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M5 15H4C2.89543 15 2 14.1046 2 13V4C2 2.89543 2.89543 2 4 2H13C14.1046 2 15 2.89543 15 4V5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button 
                  class="message-action-btn" 
                  title="重试"
                  @click="retryMessage(index)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 4V10H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M23 20V14H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10M23 14L18.36 18.36A9 9 0 0 1 3.51 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button 
                  class="message-action-btn" 
                  title="分享"
                  @click="shareMessage(message.content)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 8C19.6569 8 21 6.65685 21 5C21 3.34315 19.6569 2 18 2C16.3431 2 15 3.34315 15 5C15 5.27368 15.0522 5.53588 15.1496 5.77804L8.85041 9.22196C8.44784 8.45813 7.65685 8 6.75 8C5.23122 8 4 9.23122 4 10.75C4 12.2688 5.23122 13.5 6.75 13.5C7.65685 13.5 8.44784 13.0419 8.85041 12.278L15.1496 15.722C15.0522 15.9641 15 16.2263 15 16.5C15 18.1569 16.3431 19.5 18 19.5C19.6569 19.5 21 18.1569 21 16.5C21 14.8431 19.6569 13.5 18 13.5C17.0932 13.5 16.3022 13.9581 15.8996 14.722L9.60041 11.278C9.69797 11.0359 9.75 10.7737 9.75 10.5C9.75 10.2263 9.69797 9.96412 9.60041 9.72196L15.8996 6.27804C16.3022 7.04187 17.0932 7.5 18 7.5V8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button 
                  class="message-action-btn" 
                  :class="{ active: message.liked }"
                  title="点赞"
                  @click="toggleLike(index)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7 22V11M2 13V20C2 21.1046 2.89543 22 4 22H16.4262C17.907 22 19.1662 21.0604 19.3914 19.6126L20.4683 12.6126C20.7479 10.8209 19.2461 9.25 17.4262 9.25H14C13.4477 9.25 13 8.80228 13 8.25V5.75C13 4.23122 11.7688 3 10.25 3C9.95163 3 9.66141 3.07902 9.40691 3.22795C9.15241 3.37688 8.94271 3.59017 8.8 3.84615L5.5 9.25H4C2.89543 9.25 2 10.1454 2 11.25V13Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button 
                  class="message-action-btn" 
                  :class="{ active: message.disliked }"
                  title="点踩"
                  @click="toggleDislike(index)"
                >
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17 2V13M22 11V4C22 2.89543 21.1046 2 20 2H7.57377C6.09296 2 4.83377 2.93959 4.60858 4.38738L3.53165 11.3874C3.25212 13.1791 4.75388 14.75 6.57377 14.75H10C10.5523 14.75 11 15.1977 11 15.75V18.25C11 19.7688 12.2312 21 13.75 21C14.0484 21 14.3386 20.921 14.5931 20.772C14.8476 20.6231 15.0573 20.4098 15.2 20.1538L18.5 14.75H20C21.1046 14.75 22 13.8546 22 12.75V11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
              </div>
            </div>
          </template>
        </div>
        <div v-if="isLoading && (!messages.length || messages[messages.length - 1]?.type !== 'assistant' || !messages[messages.length - 1]?.isStreaming)" class="message assistant">
          <div class="message-content">
            <div class="message-text typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { watch, nextTick, ref, onMounted, onUnmounted } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  agentName: {
    type: String,
    required: true
  },
  messages: {
    type: Array,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  showSettingsButton: {
    type: Boolean,
    default: false
  },
  messagesContainerRef: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'open-settings', 'retry', 'copy', 'share', 'like', 'dislike', 'edit', 'resend'])

// 本地容器 ref（不依赖 props）
const messagesContainerRef = ref(null)

// 获取容器
const getContainer = () => {
  return messagesContainerRef.value
}

// 配置marked以支持markdown渲染
marked.setOptions({
  breaks: true,
  gfm: true
})

const formatMessage = (content) => {
  if (!content) return ''
  return marked(content)
}

// 编辑消息
const editingText = ref('')
const editingIndex = ref(-1)

const editMessage = (index) => {
  if (props.messages[index]) {
    editingIndex.value = index
    editingText.value = props.messages[index].content
    props.messages[index].isEditing = true
  }
}

const resendMessage = (index) => {
  if (editingIndex.value === index && editingText.value.trim()) {
    // 更新消息内容
    emit('edit', index, editingText.value.trim())
    // 退出编辑状态
    props.messages[index].isEditing = false
    editingIndex.value = -1
    const newContent = editingText.value.trim()
    editingText.value = ''
    // 触发重新发送事件
    emit('resend', index, newContent)
  } else {
    cancelEdit(index)
  }
}

const cancelEdit = (index) => {
  if (props.messages[index]) {
    props.messages[index].isEditing = false
  }
  editingIndex.value = -1
  editingText.value = ''
}

// 复制消息内容
const copyMessage = async (content) => {
  try {
    await navigator.clipboard.writeText(content)
    emit('copy', content)
    // 显示复制成功提示
    showCopyToast()
  } catch (err) {
    console.error('复制失败:', err)
  }
}

// 显示复制成功提示
const showCopyToast = () => {
  // 创建toast元素
  const toast = document.createElement('div')
  toast.textContent = '已复制'
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 0.75rem 1.25rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    z-index: 10000;
    animation: fadeInOut 2s ease;
    pointer-events: none;
  `
  
  // 添加动画样式（如果还没有）
  if (!document.getElementById('toast-styles')) {
    const style = document.createElement('style')
    style.id = 'toast-styles'
    style.textContent = `
      @keyframes fadeInOut {
        0% {
          opacity: 0;
          transform: translateY(-10px);
        }
        20% {
          opacity: 1;
          transform: translateY(0);
        }
        80% {
          opacity: 1;
          transform: translateY(0);
        }
        100% {
          opacity: 0;
          transform: translateY(-10px);
        }
      }
    `
    document.head.appendChild(style)
  }
  
  document.body.appendChild(toast)
  
  // 2秒后移除
  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast)
    }
  }, 2000)
}

// 重试消息
const retryMessage = (index) => {
  emit('retry', index)
}

// 分享消息
const shareMessage = async (content) => {
  if (navigator.share) {
    try {
      await navigator.share({
        title: '分享对话',
        text: content
      })
      emit('share', content)
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('分享失败:', err)
      }
    }
  } else {
    // 降级方案：复制到剪贴板
    copyMessage(content)
  }
}

// 点赞
const toggleLike = (index) => {
  emit('like', index)
}

// 点踩
const toggleDislike = (index) => {
  emit('dislike', index)
}

// 用户是否主动滚动了（抢占视图）
const userScrolled = ref(false)
let scrollTimeout = null
let lastScrollTop = 0
let isAutoScrolling = false
let rafId = null
let lastScrollHeight = 0
let mutationObserver = null

// 检查是否在底部附近（允许一些误差）
const isNearBottom = (container) => {
  if (!container) return false
  const threshold = 150 // 距离底部150px内认为是在底部
  const scrollTop = container.scrollTop
  const scrollHeight = container.scrollHeight
  const clientHeight = container.clientHeight
  const distanceFromBottom = scrollHeight - scrollTop - clientHeight
  return distanceFromBottom < threshold
}

// 检查 scrollHeight 是否变化，如果有变化则滚动到底部
const checkAndScroll = () => {
  const container = getContainer()
  if (!container) return
  
  const currentScrollHeight = container.scrollHeight
  
  // 如果 scrollHeight 增加了，说明有新内容
  if (currentScrollHeight > lastScrollHeight) {
    // 只有在用户没有手动滚动时才自动滚动
    if (!userScrolled.value || isNearBottom(container)) {
      scrollToBottom()
    }
    lastScrollHeight = currentScrollHeight
  } else if (currentScrollHeight !== lastScrollHeight) {
    // 如果 scrollHeight 改变了（减少或相等但容器变了），也要更新
    lastScrollHeight = currentScrollHeight
  }
}

// 滚动到底部
const scrollToBottom = (force = false) => {
  const container = getContainer()
  if (!container) return
  
  // 如果用户主动滚动了且不在底部，且不是强制滚动，则不自动滚动
  if (!force && userScrolled.value && !isNearBottom(container)) {
    return
  }
  
  // 标记为自动滚动中
  isAutoScrolling = true
  
  // 使用 requestAnimationFrame 确保DOM更新后再滚动
  if (rafId) {
    cancelAnimationFrame(rafId)
  }
  
  // 使用双重 requestAnimationFrame 确保 DOM 完全渲染
  rafId = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const currentContainer = getContainer()
        if (currentContainer && currentContainer === container) {
        const scrollHeight = container.scrollHeight
        const clientHeight = container.clientHeight
        const maxScrollTop = scrollHeight - clientHeight
        
        // 滚动到底部：设置 scrollTop 为最大值
        container.scrollTop = maxScrollTop > 0 ? maxScrollTop : 0
        
          // 在下一帧再次确认滚动到底部
          requestAnimationFrame(() => {
            const currentContainer = getContainer()
            if (currentContainer && currentContainer === container) {
            // 再次设置，确保滚动到底部
            const newScrollHeight = container.scrollHeight
            const newClientHeight = container.clientHeight
            const newMaxScrollTop = newScrollHeight - newClientHeight
            container.scrollTop = newMaxScrollTop > 0 ? newMaxScrollTop : 0
            
            // 如果滚动到底部了，重置用户滚动标志
            if (isNearBottom(container)) {
              userScrolled.value = false
            }
            // 更新最后滚动位置
            lastScrollTop = container.scrollTop
          }
          isAutoScrolling = false
          rafId = null
        })
      } else {
        isAutoScrolling = false
        rafId = null
      }
    })
  })
}

// 处理用户滚动事件
const handleScroll = () => {
  const container = getContainer()
  if (!container) return
  
  const currentScrollTop = container.scrollTop
  const scrollDifference = currentScrollTop - lastScrollTop
  
  // 如果用户明显向上滚动（差值大于10px），无论是否在自动滚动，都允许用户抢占
  if (scrollDifference < -10) {
    // 取消正在进行的自动滚动
    if (rafId) {
      cancelAnimationFrame(rafId)
      rafId = null
    }
    isAutoScrolling = false
    
    // 如果不在底部，标记为用户手动滚动
    if (!isNearBottom(container)) {
      userScrolled.value = true
    }
  }
  // 如果正在自动滚动且用户向下滚动，可能是自动滚动导致的，暂时忽略
  else if (isAutoScrolling && scrollDifference > 0) {
    // 自动滚动中向下滚动，暂时忽略
    return
  }
  
  // 清除之前的定时器
  if (scrollTimeout) {
    clearTimeout(scrollTimeout)
  }
  
  // 判断用户是否向上滚动（查看历史消息）
  // 只有当用户明显向上滚动（差值大于5px，避免误判）且不在底部时，才标记为用户滚动
  if (scrollDifference < -5 && !isNearBottom(container)) {
    userScrolled.value = true
  } 
  // 如果用户滚动到接近底部（在阈值内），重置标志，允许自动滚动
  else if (isNearBottom(container)) {
    userScrolled.value = false
  }
  // 如果用户向下滚动且到达底部，重置标志
  else if (scrollDifference > 0 && isNearBottom(container)) {
    userScrolled.value = false
  }
  
  lastScrollTop = currentScrollTop
  
  // 设置一个短暂的延迟，再次检查是否还在底部附近
  scrollTimeout = setTimeout(() => {
    const container = getContainer()
    if (container) {
      if (isNearBottom(container)) {
        userScrolled.value = false
      }
    }
  }, 200)
}

// 监听消息变化，自动滚动
watch(() => props.messages.length, () => {
  nextTick(() => {
    // 使用双重 nextTick 确保 DOM 完全更新
    nextTick(() => {
      scrollToBottom(true) // 强制滚动
    })
  })
})

// 监听消息内容变化（打字机效果）- 监听所有助手消息的内容变化
watch(() => {
  // 获取最后一个助手消息的内容长度，用于检测内容变化
  const lastMsg = props.messages[props.messages.length - 1]
  if (lastMsg && lastMsg.type === 'assistant') {
    return lastMsg.content?.length || 0
  }
  return 0
}, () => {
  // 对于内容更新，只有在用户没有手动滚动时才自动滚动
  scrollToBottom()
}, { flush: 'post' })

// 监听加载状态
watch(() => props.isLoading, (newVal) => {
  if (newVal) {
    nextTick(() => {
      scrollToBottom(true) // 加载时强制滚动
    })
  }
})

// 监听本地 messagesContainerRef 的变化
watch(() => messagesContainerRef.value, (container, oldContainer) => {
  // 移除旧容器的监听
  if (oldContainer && oldContainer.hasAttribute('data-scroll-listener')) {
    oldContainer.removeEventListener('scroll', handleScroll)
    oldContainer.removeAttribute('data-scroll-listener')
  }
  
  // 断开旧的 MutationObserver
  if (mutationObserver) {
    mutationObserver.disconnect()
    mutationObserver = null
  }
  
  // 添加新容器的监听
  if (container && !container.hasAttribute('data-scroll-listener')) {
    container.addEventListener('scroll', handleScroll, { passive: true })
    container.setAttribute('data-scroll-listener', 'true')
    lastScrollTop = container.scrollTop
    lastScrollHeight = container.scrollHeight
    userScrolled.value = false // 重置用户滚动标志
    
    // 使用 MutationObserver 监听 DOM 变化，当有变化时检查 scrollHeight
    mutationObserver = new MutationObserver(() => {
      // 使用 requestAnimationFrame 确保 DOM 更新后再检查
      requestAnimationFrame(() => {
        checkAndScroll()
      })
    })
    mutationObserver.observe(container, {
      childList: true,
      subtree: true,
      characterData: true
    })
    
    // 初始滚动到底部
    nextTick(() => {
      setTimeout(() => {
        scrollToBottom(true)
        lastScrollHeight = container.scrollHeight
      }, 100)
    })
  }
}, { immediate: true })

// 挂载时添加滚动监听（作为备用）
onMounted(() => {
  // 延迟一下，确保 ref 已经绑定
  nextTick(() => {
    setTimeout(() => {
      const container = getContainer()
      if (container) {
        if (!container.hasAttribute('data-scroll-listener')) {
          container.addEventListener('scroll', handleScroll, { passive: true })
          container.setAttribute('data-scroll-listener', 'true')
          lastScrollTop = container.scrollTop
          userScrolled.value = false // 重置用户滚动标志
          // 初始滚动到底部
          scrollToBottom(true)
        }
      }
    }, 100)
  })
})

// 卸载时移除滚动监听
onUnmounted(() => {
  const container = getContainer()
  if (container) {
    container.removeEventListener('scroll', handleScroll)
    container.removeAttribute('data-scroll-listener')
  }
  if (mutationObserver) {
    mutationObserver.disconnect()
    mutationObserver = null
  }
  if (scrollTimeout) {
    clearTimeout(scrollTimeout)
  }
  if (rafId) {
    cancelAnimationFrame(rafId)
  }
})
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
  position: relative;
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
  min-height: 0;
  height: 100%;
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
  flex-shrink: 0;
}

.agent-detail-title {
  font-size: 1.125rem;
  font-weight: 600;
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

.messages-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 2rem;
  padding-bottom: 200px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: transparent;
  min-height: 0;
  max-height: 100%;
  height: 0; /* 关键：配合 flex: 1 使用，确保容器有高度限制，这样才能产生滚动条 */
  /* 移除 scroll-behavior，让 JavaScript 控制滚动行为 */
}

.message {
  display: flex;
  flex-direction: column;
  animation: fadeIn 0.3s ease;
}

.message.user {
  align-items: flex-end;
}

.message.assistant {
  align-items: flex-start;
}

.message-content {
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  word-wrap: break-word;
}

.message.user .message-content {
  background: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.message.assistant .message-content {
  width: 100%;
  max-width: 100%;
  background: transparent;
  border: none;
  padding: 0.75rem 0;
}

.message-text {
  color: var(--text-primary);
  font-size: 0.875rem;
  line-height: 1.6;
}

.message-wrapper {
  position: relative;
  width: 100%;
}

.user-message-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  max-width: 70%;
}

.user-message-container:hover .user-message-actions {
  opacity: 1;
}

.message-edit-input {
  width: 100%;
  min-height: 60px;
  padding: 0.75rem 1rem;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 0.5rem;
  color: var(--text-primary);
  font-size: 0.875rem;
  line-height: 1.6;
  font-family: inherit;
  resize: vertical;
  outline: none;
}

.message-edit-input:focus {
  border-color: rgba(59, 130, 246, 0.5);
  background: rgba(59, 130, 246, 0.15);
}

.user-message-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.user-message-actions.edit-actions {
  opacity: 1;
}

.edit-btn,
.cancel-btn {
  width: 24px;
  height: 24px;
  padding: 0;
}

.edit-btn {
  color: rgb(59, 130, 246);
}

.edit-btn:hover {
  background: rgba(59, 130, 246, 0.2);
  color: rgb(96, 165, 250);
}

.cancel-btn {
  color: var(--text-secondary);
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.edit-btn svg,
.cancel-btn svg {
  width: 16px;
  height: 16px;
}

.message-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.message-action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: transparent;
  border: none;
  border-radius: 0.25rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.message-action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.message-action-btn.active {
  color: rgb(59, 130, 246);
}

.message-action-btn svg {
  width: 14px;
  height: 14px;
}

.markdown-content {
  word-wrap: break-word;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin: 0.75rem 0 0.5rem 0;
  font-weight: 600;
  line-height: 1.4;
}

.markdown-content :deep(h1) {
  font-size: 1.25rem;
}

.markdown-content :deep(h2) {
  font-size: 1.125rem;
}

.markdown-content :deep(h3) {
  font-size: 1rem;
}

.markdown-content :deep(p) {
  margin: 0.5rem 0;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.markdown-content :deep(li) {
  margin: 0.25rem 0;
}

.markdown-content :deep(code) {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.8125rem;
  font-family: 'Courier New', monospace;
}

.markdown-content :deep(pre) {
  background: rgba(0, 0, 0, 0.3);
  padding: 0.75rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin: 0.75rem 0;
}

.markdown-content :deep(pre code) {
  background: transparent;
  padding: 0;
}

.markdown-content :deep(blockquote) {
  border-left: 3px solid rgba(255, 255, 255, 0.3);
  padding-left: 1rem;
  margin: 0.75rem 0;
  color: var(--text-secondary);
}

.markdown-content :deep(a) {
  color: rgb(59, 130, 246);
  text-decoration: underline;
}

.markdown-content :deep(a:hover) {
  color: rgb(96, 165, 250);
}

.message-text.typing {
  display: flex;
  gap: 0.25rem;
}

.message-text.typing span {
  width: 8px;
  height: 8px;
  background: var(--text-secondary);
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.message-text.typing span:nth-child(2) {
  animation-delay: 0.2s;
}

.message-text.typing span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>


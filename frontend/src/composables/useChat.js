import { ref, nextTick, watch } from 'vue'
import { askQuestionStream, getErrorMessage } from '../utils/api'

/**
 * 聊天功能组合式函数
 * @param {Ref} messagesContainer - 消息容器的ref
 * @returns {Object} 聊天相关状态和方法
 */
export function useChat(messagesContainer) {
  const messages = ref([])
  const currentQuestion = ref('')
  const isLoading = ref(false)
  let typingTimer = null
  let userScrolled = false
  let isAutoScrolling = false

  // 检测用户是否手动滚动
  const handleScroll = () => {
    if (isAutoScrolling) {
      isAutoScrolling = false
      return
    }
    
    if (!messagesContainer.value) return
    
    const container = messagesContainer.value
    const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100
    
    if (isNearBottom) {
      userScrolled = false
    } else {
      userScrolled = true
    }
  }

  // 添加滚动监听
  const setupScrollListener = () => {
    if (messagesContainer.value && !messagesContainer.value.hasAttribute('data-scroll-listener')) {
      messagesContainer.value.addEventListener('scroll', handleScroll, { passive: true })
      messagesContainer.value.setAttribute('data-scroll-listener', 'true')
    }
  }

  // 智能滚动到底部
  const scrollToBottom = (force = false) => {
    if (!messagesContainer.value) return
    
    // 如果用户手动滚动了，且不是强制滚动，则不自动滚动
    if (userScrolled && !force) {
      return
    }
    
    isAutoScrolling = true
    nextTick(() => {
      if (messagesContainer.value) {
        const container = messagesContainer.value
        container.scrollTop = container.scrollHeight
        // 重置用户滚动状态（如果已经滚动到底部）
        const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100
        if (isNearBottom) {
          userScrolled = false
        }
      }
      isAutoScrolling = false
    })
  }

  // 监听消息容器ref变化，设置滚动监听
  watch(() => messagesContainer.value, (newVal) => {
    if (newVal) {
      setupScrollListener()
    }
  }, { immediate: true })

  // 监听消息变化，自动滚动
  watch(() => messages.value.length, () => {
    setupScrollListener()
    scrollToBottom()
  }, { flush: 'post' })

  // 监听消息内容变化，自动滚动
  watch(() => messages.value.map(m => m.content).join(''), () => {
    setupScrollListener()
    scrollToBottom()
  }, { flush: 'post' })

  const sendQuestion = async () => {
    if (!currentQuestion.value.trim() || isLoading.value) return

    const question = currentQuestion.value.trim()
    messages.value.push({
      type: 'user',
      content: question
    })

    currentQuestion.value = ''
    isLoading.value = true

    await nextTick()
    scrollToBottom(true) // 强制滚动

    // 创建助手消息，初始内容为空
    const assistantMessageIndex = messages.value.length
    messages.value.push({
      type: 'assistant',
      content: '',
      isStreaming: true,
      liked: false,
      disliked: false
    })

    await nextTick()
    scrollToBottom(true) // 强制滚动

    let accumulatedContent = ''
    let charIndex = 0
    let isTyping = false
    let streamComplete = false
    let checkInterval = null

    // 打字机效果函数
    const typeWriter = () => {
      if (charIndex < accumulatedContent.length) {
        const displayContent = accumulatedContent.slice(0, charIndex + 1)
        messages.value[assistantMessageIndex].content = displayContent
        messages.value[assistantMessageIndex].isStreaming = true
        charIndex++
        scrollToBottom()
        typingTimer = setTimeout(typeWriter, 15) // 每15ms显示一个字符
        isTyping = true
      } else {
        // 当前累积内容已显示完
        isTyping = false
        // 如果流式响应已完成，标记为完成
        if (streamComplete) {
          messages.value[assistantMessageIndex].isStreaming = false
          isLoading.value = false
          if (checkInterval) {
            clearInterval(checkInterval)
            checkInterval = null
          }
        }
      }
    }

    // 启动打字机效果
    const startTyping = () => {
      if (!isTyping && accumulatedContent.length > charIndex) {
        typeWriter()
      }
    }

    try {
      await askQuestionStream(question, 'default', (chunk) => {
        // 检查消息是否还存在
        if (!messages.value[assistantMessageIndex]) {
          return
        }
        
        if (chunk.type === 'content' || chunk.type === 'delta') {
          // 累积内容
          const newContent = chunk.content || ''
          if (newContent) {
            accumulatedContent += newContent
            startTyping()
          }
        } else if (chunk.type === 'done') {
          // 流式响应完成
          streamComplete = true
          // 如果打字机已完成，直接标记为完成
          if (!isTyping) {
            if (messages.value[assistantMessageIndex]) {
              messages.value[assistantMessageIndex].isStreaming = false
            }
            isLoading.value = false
            scrollToBottom()
          }
        } else if (chunk.type === 'error') {
          // 处理错误
          clearTimeout(typingTimer)
          if (checkInterval) {
            clearInterval(checkInterval)
            checkInterval = null
          }
          if (messages.value[assistantMessageIndex]) {
            messages.value[assistantMessageIndex] = {
              type: 'assistant',
              content: chunk.content || '抱歉，发生了错误。',
              isStreaming: false,
              liked: false,
              disliked: false
            }
          }
          isLoading.value = false
          streamComplete = true
          scrollToBottom()
        }
      })

      // 流式响应完成，确保所有内容都显示完成
      streamComplete = true
      
      // 如果还有未显示的内容，继续显示
      if (messages.value[assistantMessageIndex]) {
        if (charIndex < accumulatedContent.length) {
          // 继续打字机效果直到完成
          if (!isTyping) {
            typeWriter()
          }
          // 设置检查，确保最终完成
          checkInterval = setInterval(() => {
            if (!messages.value[assistantMessageIndex]) {
              clearInterval(checkInterval)
              checkInterval = null
              return
            }
            if (!isTyping && charIndex >= accumulatedContent.length) {
              clearInterval(checkInterval)
              checkInterval = null
              if (messages.value[assistantMessageIndex]) {
                messages.value[assistantMessageIndex].isStreaming = false
              }
              isLoading.value = false
              scrollToBottom()
            }
          }, 100)
        } else if (accumulatedContent.length > 0) {
          // 所有内容已显示完成
          if (messages.value[assistantMessageIndex]) {
            messages.value[assistantMessageIndex].isStreaming = false
          }
          isLoading.value = false
          scrollToBottom()
        } else {
          // 没有收到任何内容
          if (messages.value[assistantMessageIndex]) {
            messages.value[assistantMessageIndex] = {
              type: 'assistant',
              content: '抱歉，未能获取到回答。请稍后重试。',
              isStreaming: false,
              liked: false,
              disliked: false
            }
          }
          isLoading.value = false
          scrollToBottom()
        }
      }
    } catch (error) {
      console.error('Error sending question:', error)
      clearTimeout(typingTimer)
      if (checkInterval) {
        clearInterval(checkInterval)
        checkInterval = null
      }
      messages.value[assistantMessageIndex] = {
        type: 'assistant',
        content: getErrorMessage(error),
        isStreaming: false,
        liked: false,
        disliked: false
      }
      isLoading.value = false
      streamComplete = true
      await nextTick()
      scrollToBottom()
    }
  }

  const clearMessages = () => {
    messages.value = []
    currentQuestion.value = ''
  }

  /**
   * 根据时间获取问候语
   */
  const getTimeGreeting = () => {
    const hour = new Date().getHours()
    if (hour >= 5 && hour < 12) {
      return '早上好'
    } else if (hour >= 12 && hour < 14) {
      return '中午好'
    } else if (hour >= 14 && hour < 18) {
      return '下午好'
    } else if (hour >= 18 && hour < 22) {
      return '晚上好'
    } else {
      return '晚上好'
    }
  }

  /**
   * 生成随机的问候语模板
   */
  const getRandomGreetingTemplate = (agentName) => {
    const greeting = getTimeGreeting()
    const templates = [
      `${greeting}！我是${agentName}，很高兴为你服务。有什么问题尽管问我吧！`,
      `${greeting}！我是${agentName}，随时为你提供帮助。`,
      `${greeting}！欢迎使用${agentName}，我会尽力解答你的问题。`,
      `${greeting}！我是${agentName}，有什么需要帮助的吗？`,
      `${greeting}！${agentName}为你服务，请随时提问。`,
      `${greeting}！我是${agentName}，很高兴认识你，有什么问题都可以问我。`,
      `${greeting}！欢迎使用${agentName}，我会认真回答你的每一个问题。`,
      `${greeting}！我是${agentName}，随时准备为你提供专业的帮助。`
    ]
    return templates[Math.floor(Math.random() * templates.length)]
  }

  /**
   * 使用打字机效果显示文本
   */
  const typeWriterEffect = (text, messageIndex, onComplete) => {
    let charIndex = 0
    const typeWriter = () => {
      // 检查消息是否还存在
      if (!messages.value[messageIndex]) {
        if (typingTimer) {
          clearTimeout(typingTimer)
          typingTimer = null
        }
        return
      }
      
      if (charIndex < text.length) {
        const displayContent = text.slice(0, charIndex + 1)
        if (messages.value[messageIndex]) {
          messages.value[messageIndex].content = displayContent
          messages.value[messageIndex].isStreaming = true
        }
        charIndex++
        scrollToBottom()
        typingTimer = setTimeout(typeWriter, 30) // 每30ms显示一个字符，比回答稍慢一些
      } else {
        // 打字完成
        if (messages.value[messageIndex]) {
          messages.value[messageIndex].isStreaming = false
        }
        if (onComplete) {
          onComplete()
        }
      }
    }
    typeWriter()
  }

  const addWelcomeMessage = (agentName) => {
    const welcomeText = getRandomGreetingTemplate(agentName)
    const messageIndex = messages.value.length
    messages.value.push({
      type: 'assistant',
      content: '',
      isStreaming: true,
      liked: false,
      disliked: false
    })
    nextTick(() => {
      scrollToBottom()
      typeWriterEffect(welcomeText, messageIndex, () => {
        scrollToBottom()
      })
    })
  }

  return {
    messages,
    currentQuestion,
    isLoading,
    sendQuestion,
    clearMessages,
    scrollToBottom,
    addWelcomeMessage
  }
}


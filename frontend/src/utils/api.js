// API基础URL
const API_BASE_URL = 'http://localhost:8000'

/**
 * 发送问题到API（非流式）
 * @param {string} question - 用户问题
 * @param {string} companyId - 公司ID，默认为'default'
 * @returns {Promise<{answer: string}>}
 */
export async function askQuestion(question, companyId = 'default') {
  const response = await fetch(`${API_BASE_URL}/api/qa`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question,
      company_id: companyId,
      stream: false
    })
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`HTTP ${response.status}: ${errorText}`)
  }

  return await response.json()
}

/**
 * 发送问题到API（流式响应）
 * @param {string} question - 用户问题
 * @param {string} companyId - 公司ID，默认为'default'
 * @param {Function} onChunk - 接收每个chunk的回调函数，参数为 {type: string, content: string}
 * @returns {Promise<void>}
 */
export async function askQuestionStream(question, companyId = 'default', onChunk) {
  const response = await fetch(`${API_BASE_URL}/api/qa`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question,
      company_id: companyId,
      stream: true
    })
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`HTTP ${response.status}: ${errorText}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  try {
    while (true) {
      const { done, value } = await reader.read()
      
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n\n')
      buffer = lines.pop() || '' // 保留最后一个不完整的行

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6) // 移除 'data: ' 前缀
          
          if (data === '[DONE]') {
            return
          }

          try {
            const chunk = JSON.parse(data)
            if (onChunk) {
              onChunk(chunk)
            }
          } catch (e) {
            console.error('解析chunk失败:', e, data)
          }
        }
      }
    }
  } finally {
    reader.releaseLock()
  }
}

/**
 * 获取错误消息
 * @param {Error} error - 错误对象
 * @returns {string} 用户友好的错误消息
 */
export function getErrorMessage(error) {
  if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError') || error.name === 'TypeError') {
    return '无法连接到服务器，请检查网络连接或确认后端服务是否已启动（http://localhost:8000）。'
  } else if (error.message.includes('404')) {
    return 'API接口不存在，请检查后端服务配置。'
  } else if (error.message.includes('500')) {
    return '服务器内部错误，请稍后再试。'
  } else if (error.message.includes('HTTP')) {
    return `服务器错误: ${error.message}`
  }
  return '抱歉，发生了错误。请稍后再试。'
}


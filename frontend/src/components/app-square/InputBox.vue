<template>
  <div class="input-section" :class="{ 'input-section-fixed': isFixed, 'input-card': isFixed, 'sidebar-collapsed': isSidebarCollapsed, 'input-section-enter': !isFixed }">
    <div class="input-container">
      <h2 v-if="showTitle" class="input-section-title">{{ title }}</h2>
      <p v-if="showDescription" class="input-section-description">{{ description }}</p>
      <div class="input-wrapper">
        <textarea
          v-model="inputValue"
          class="question-input"
          :placeholder="placeholder"
          @focus="handleFocus"
          @blur="handleBlur"
          @keydown.enter.exact.prevent="handleEnter"
          @keydown.shift.enter.exact="inputValue += '\n'"
          rows="3"
        ></textarea>
        <div class="input-actions">
          <button class="action-icon-btn" title="语音输入">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M19 10V12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12V10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 19V23" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M8 23H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="action-icon-btn" title="附件">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21.44 11.05L12.25 20.24C11.1242 21.3658 9.59723 21.9983 8.005 21.9983C6.41277 21.9983 4.88578 21.3658 3.76 20.24C2.63422 19.1142 2.00171 17.5872 2.00171 15.995C2.00171 14.4028 2.63422 12.8758 3.76 11.75L12.95 2.56C13.7006 1.80944 14.7185 1.3877 15.78 1.3877C16.8415 1.3877 17.8594 1.80944 18.61 2.56C19.3606 3.31056 19.7823 4.32845 19.7823 5.39C19.7823 6.45155 19.3606 7.46944 18.61 8.22L9.41 17.41C9.03482 17.7852 8.52574 17.9961 7.995 17.9961C7.46426 17.9961 6.95518 17.7852 6.58 17.41C6.20482 17.0348 5.99393 16.5257 5.99393 15.995C5.99393 15.4643 6.20482 14.9552 6.58 14.58L15.07 6.09" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button 
            class="submit-btn" 
            @click="handleSubmit" 
            :disabled="disabled"
            title="发送"
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 5V19M12 5L5 12M12 5L19 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
      <!-- 行业标签选择（在输入框下方左侧） -->
      <div v-if="showIndustryTags" class="industry-tags-container">
        <!-- 预设行业标签 -->
        <div
          v-for="tag in industryTags"
          :key="tag.id"
          class="industry-tag"
          :class="{ 'industry-tag-active': selectedIndustry === tag.id }"
          @click="$emit('select-industry', tag.id)"
        >
          {{ tag.name }}
        </div>
        
        <!-- 自定义标签 -->
        <div
          v-for="(customTag, index) in customTags"
          :key="'custom-' + index"
          class="industry-tag industry-tag-custom"
          :class="{ 'industry-tag-active': selectedCustomTags && selectedCustomTags.includes(customTag) }"
          @click="$emit('select-custom-tag', customTag)"
        >
          {{ customTag }}
          <button
            class="custom-tag-remove"
            @click.stop="$emit('remove-custom-tag', customTag)"
            title="删除"
          >
            ×
          </button>
        </div>
        
        <!-- 添加自定义标签输入框 -->
        <div class="custom-tag-input-wrapper">
          <input
            v-model="customTagInput"
            type="text"
            class="custom-tag-input"
            placeholder="+ 添加标签"
            @keydown.enter.prevent="handleAddCustomTag"
            @blur="handleAddCustomTag"
            maxlength="10"
          />
        </div>
      </div>
      
      <div v-if="showExamples && examples.length > 0" class="example-questions">
        <div
          v-for="(example, index) in examples"
          :key="index"
          class="example-item"
          @click="$emit('fill-example', example.text)"
        >
          <DomainIcon :icon="example.icon" class="example-icon" />
          <div class="example-content">
            <div class="example-text">{{ example.text }}</div>
          </div>
          <div class="example-arrow">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M7 17L17 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7 7H17V17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import DomainIcon from './DomainIcon.vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '尽管问...'
  },
  isFixed: {
    type: Boolean,
    default: false
  },
  isSidebarCollapsed: {
    type: Boolean,
    default: false
  },
  showTitle: {
    type: Boolean,
    default: true
  },
  showDescription: {
    type: Boolean,
    default: true
  },
  showExamples: {
    type: Boolean,
    default: true
  },
  title: {
    type: String,
    default: '应用广场'
  },
  description: {
    type: String,
    default: '探索AI在各个领域的智能应用，选择适合您需求的Agent开始体验'
  },
  examples: {
    type: Array,
    default: () => []
  },
  disabled: {
    type: Boolean,
    default: false
  },
  showIndustryTags: {
    type: Boolean,
    default: false
  },
  industryTags: {
    type: Array,
    default: () => []
  },
  selectedIndustry: {
    type: String,
    default: null
  },
  customTags: {
    type: Array,
    default: () => []
  },
  selectedCustomTags: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'focus', 'blur', 'fill-example', 'select-industry', 'add-custom-tag', 'select-custom-tag', 'remove-custom-tag'])

const customTagInput = ref('')

const handleAddCustomTag = () => {
  const tag = customTagInput.value.trim()
  if (tag && !props.customTags.includes(tag)) {
    emit('add-custom-tag', tag)
    customTagInput.value = ''
  }
}

const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleFocus = () => {
  emit('focus')
}

const handleBlur = () => {
  emit('blur')
}

const handleEnter = () => {
  if (inputValue.value.trim() && !props.disabled) {
    handleSubmit()
  }
}

const handleSubmit = () => {
  if (inputValue.value.trim() && !props.disabled) {
    emit('submit', inputValue.value)
  }
}
</script>

<style scoped>
.input-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: transparent;
}

.input-section:not(.input-section-fixed) {
  width: 100%;
}

.input-section-enter {
  animation: fadeInScale 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.input-section-fixed {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 1.5rem;
  padding-bottom: 1.5rem;
  flex: none;
  justify-content: flex-end;
  transition: left 0.3s ease;
  background: transparent;
  width: 100%;
}

.input-section-fixed.sidebar-collapsed {
  left: 0;
}

.input-card {
  background: transparent;
  border: none;
  border-radius: 0;
  backdrop-filter: none;
}

.input-container {
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
}

.input-section-fixed .input-container {
  max-width: 100%;
  width: 100%;
  margin: 0 auto;
}

.input-section-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.75rem 0;
  text-align: center;
  width: 100%;
}

.input-section-description {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0 0 2rem 0;
  text-align: center;
  width: 100%;
  line-height: 1.6;
}

.input-section-fixed .input-section-title,
.input-section-fixed .input-section-description {
  display: none;
}

.input-wrapper {
  position: relative;
  background: rgba(30, 30, 30, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem;
  padding-bottom: 4rem;
  transition: all 0.3s ease;
  min-height: 120px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.input-section-fixed .input-wrapper {
  margin: 0;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  background: rgba(30, 30, 30, 0.8);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.input-wrapper:focus-within {
  border-color: rgba(59, 130, 246, 0.5);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
  background: rgba(35, 35, 35, 0.9);
}

.question-input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 400;
  font-family: inherit;
  padding: 0;
  padding-right: 180px;
  line-height: 1.6;
  min-height: 3rem;
  resize: none;
  overflow-y: auto;
  text-align: left;
  vertical-align: top;
}

.question-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
  opacity: 0.7;
  font-size: 0.875rem;
}

.input-actions {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
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
  width: 20px;
  height: 20px;
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.5);
  color: #3b82f6;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.submit-btn:hover:not(:disabled) {
  background: rgba(59, 130, 246, 0.3);
  border-color: rgba(59, 130, 246, 0.7);
  color: #60a5fa;
  transform: scale(1.05);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn svg {
  width: 20px;
  height: 20px;
}

.industry-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  margin-top: 1rem;
  align-self: flex-start;
  width: 100%;
  align-items: center;
}

.industry-tag {
  padding: 0.25rem 0.625rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  color: var(--text-secondary);
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  height: 1.75rem;
  line-height: 1;
}

.industry-tag:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: var(--text-primary);
}

.industry-tag-active {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.5);
  color: #3b82f6;
}

.industry-tag-active:hover {
  background: rgba(59, 130, 246, 0.3);
  border-color: rgba(59, 130, 246, 0.7);
}

.industry-tag-custom {
  padding-right: 0.375rem;
}

.custom-tag-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1rem;
  height: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  color: var(--text-secondary);
  font-size: 0.875rem;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
  margin-left: 0.125rem;
}

.custom-tag-remove:hover {
  background: rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.custom-tag-input-wrapper {
  display: inline-flex;
  align-items: center;
}

.custom-tag-input {
  padding: 0.25rem 0.625rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px dashed rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  color: var(--text-secondary);
  font-size: 0.75rem;
  outline: none;
  transition: all 0.2s ease;
  height: 1.75rem;
  line-height: 1;
  width: 5rem;
}

.custom-tag-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.custom-tag-input:focus {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(59, 130, 246, 0.5);
  color: var(--text-primary);
  width: 6rem;
}

.example-questions {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-top: 1.5rem;
}

.example-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 0;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.example-item:last-child {
  border-bottom: none;
}

.example-item:hover {
  padding-left: 0.5rem;
}

.example-icon {
  width: 20px;
  height: 20px;
  color: var(--text-secondary);
}

.example-content {
  flex: 1;
  min-width: 0;
}

.example-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
  transition: color 0.2s ease;
}

.example-item:hover .example-text {
  color: var(--text-primary);
}

.example-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  opacity: 0;
  transform: translateX(-4px);
  transition: all 0.2s ease;
  color: var(--text-secondary);
}

.example-item:hover .example-arrow {
  opacity: 1;
  transform: translateX(0);
  color: var(--text-primary);
}

.example-arrow svg {
  width: 100%;
  height: 100%;
  stroke: currentColor;
  fill: none;
}

@media (max-width: 1024px) {
  .input-section-fixed {
    left: 460px;
  }

  .input-section-fixed.sidebar-collapsed {
    left: 360px;
  }
}

@media (max-width: 768px) {
  .input-section-fixed {
    left: 440px;
    padding: 1rem 1.5rem;
  }

  .input-section-fixed.sidebar-collapsed {
    left: 300px;
  }
}
</style>


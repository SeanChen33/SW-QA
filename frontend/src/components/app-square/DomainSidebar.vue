<template>
  <aside class="domain-sidebar" :class="{ collapsed: isCollapsed }">
    <div v-if="!isCollapsed" class="sidebar-header">
      <Logo class="sidebar-logo" />
      <div class="sidebar-title">{{ title || '应用广场' }}</div>
    </div>
    <div v-else class="sidebar-header-collapsed">
      <Logo class="sidebar-logo-icon" />
    </div>
    
    <div class="sidebar-actions">
      <button 
        :class="isCollapsed ? 'home-button-icon' : 'home-button'" 
        @click="$emit('go-home')"
        :title="isCollapsed ? '回到主页' : ''"
      >
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span v-if="!isCollapsed">回到主页</span>
      </button>
    </div>
    
    <div class="domain-list">
      <div
        v-for="domain in domains"
        :key="domain.id"
        class="domain-item"
        :class="{ active: selectedDomain === domain.id, collapsed: isCollapsed }"
        @click="$emit('select-domain', domain.id)"
        :title="isCollapsed ? domain.name : ''"
      >
        <DomainIcon :icon="domain.icon" />
        <span v-if="!isCollapsed" class="domain-name">{{ domain.name }}</span>
      </div>
    </div>
    
    <div class="sidebar-footer">
      <button class="sidebar-toggle" @click="$emit('toggle')" :title="isCollapsed ? '展开菜单' : '收缩菜单'">
        <svg v-if="!isCollapsed" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </aside>
</template>

<script setup>
import Logo from '../Logo.vue'
import DomainIcon from './DomainIcon.vue'

defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  },
  domains: {
    type: Array,
    required: true
  },
  selectedDomain: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: '应用广场'
  }
})

defineEmits(['go-home', 'select-domain', 'toggle'])
</script>

<style scoped>
.domain-sidebar {
  width: 240px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  will-change: width;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.domain-sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar-header-collapsed {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: center;
}

.sidebar-logo {
  width: 32px;
  height: 32px;
}

.sidebar-logo-icon {
  width: 32px;
  height: 32px;
}

.sidebar-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
}

.sidebar-actions {
  padding: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.home-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  background: transparent;
  border: none;
  border-radius: 0.5rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.home-button span {
  white-space: nowrap;
}

.home-button:hover {
  background: rgba(255, 255, 255, 0.05);
}

.home-button svg {
  width: 18px;
  height: 18px;
}

.home-button-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.75rem;
  background: transparent;
  border: none;
  border-radius: 0.5rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.home-button-icon:hover {
  background: rgba(255, 255, 255, 0.05);
}

.home-button-icon svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.domain-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.domain-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.domain-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0.875rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
  position: relative;
}

.domain-item.collapsed {
  padding: 0.75rem;
  justify-content: center;
}

.domain-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.domain-item.active {
  color: var(--primary-color);
  background: transparent;
}

.domain-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0.5rem;
  right: 0.5rem;
  height: 2px;
  background: linear-gradient(90deg, #000000 0%, #8b5cf6 100%);
  border-radius: 1px;
}

.domain-item.collapsed.active::after {
  left: 0.25rem;
  right: 0.25rem;
}

.domain-name {
  font-size: 0.875rem;
  flex: 1;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s ease 0.1s;
  will-change: opacity;
}

.domain-sidebar:not(.collapsed) .domain-name {
  opacity: 1;
}

.sidebar-footer {
  padding: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-toggle {
  width: 100%;
  padding: 0.75rem;
  background: transparent;
  border: none;
  border-radius: 0.5rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
}

.domain-sidebar.collapsed .sidebar-toggle {
  background: transparent;
  border: none;
}

.domain-sidebar.collapsed .sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
}

.sidebar-toggle svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: block;
}
</style>


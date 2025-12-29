<template>
  <aside class="agent-list-sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <div class="agent-list-header">
      <DomainIcon :icon="domainIcon" class="agent-list-icon" />
      <h3 class="agent-list-title">{{ domainName }}</h3>
    </div>
    <div class="agent-list-content">
      <div class="agent-grid">
        <div
          v-for="agent in agents"
          :key="agent.id"
          class="agent-card"
          :class="{ 
            active: selectedAgentId === agent.id
          }"
          @click="$emit('select-agent', agent)"
        >
          <div class="agent-card-header">
            <h4 class="agent-card-title">{{ agent.name }}</h4>
            <span v-if="agent.domain" class="agent-domain-tag">{{ getDomainTag(agent.domain) }}</span>
            <span v-if="agent.matchScore && agent.matchScore > 0" class="match-indicator" title="匹配度">✓</span>
          </div>
          <p class="agent-card-description">{{ agent.description }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import DomainIcon from './DomainIcon.vue'
import { DOMAIN_TAG_MAP } from '../../utils/constants'

const props = defineProps({
  isSidebarCollapsed: {
    type: Boolean,
    default: false
  },
  domainName: {
    type: String,
    required: true
  },
  domainIcon: {
    type: String,
    required: true
  },
  agents: {
    type: Array,
    required: true
  },
  selectedAgentId: {
    type: Number,
    default: null
  }
})

defineEmits(['select-agent'])

const getDomainTag = (domain) => {
  return DOMAIN_TAG_MAP[domain] || domain
}
</script>

<style scoped>
.agent-list-sidebar {
  width: 280px;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: fixed;
  left: 240px;
  top: 0;
  z-index: 99;
  transition: left 0.3s ease, width 0.3s ease;
}

.agent-list-sidebar.sidebar-collapsed {
  left: 60px;
}

.agent-list-header {
  padding: 0 1rem 1rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.agent-list-icon {
  width: 20px;
  height: 20px;
  color: var(--text-primary);
}

.agent-list-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.agent-list-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 1rem 1rem;
}

.agent-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.agent-card {
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.agent-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #000000 0%, #8b5cf6 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.agent-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.agent-card:hover::before {
  transform: scaleX(1);
}

.agent-card.active {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.5);
}

.agent-card.active::before {
  transform: scaleX(1);
}

.agent-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.agent-card-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
}

.agent-domain-tag {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  background: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 0.25rem;
  color: rgb(96, 165, 250);
  white-space: nowrap;
  flex-shrink: 0;
}

.match-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.5);
  border-radius: 50%;
  color: #22c55e;
  font-size: 0.75rem;
  font-weight: bold;
  flex-shrink: 0;
}

.agent-card-description {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}
</style>


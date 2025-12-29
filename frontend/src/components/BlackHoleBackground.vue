<template>
    <div class="blackhole-background">
      <div class="blackhole-container">
        <!-- 外层旋转环 -->
        <div class="ring ring-1"></div>
        <div class="ring ring-2"></div>
        <div class="ring ring-3"></div>
        
        <!-- 吸积盘 -->
        <div class="accretion-disk">
          <div class="disk-segment disk-1"></div>
          <div class="disk-segment disk-2"></div>
          <div class="disk-segment disk-3"></div>
          <div class="disk-segment disk-4"></div>
        </div>
        
        <!-- 中心黑洞 -->
        <div class="event-horizon">
          <div class="singularity"></div>
        </div>
        
        <!-- 光线扭曲效果 -->
        <div class="light-rays">
          <div class="ray ray-1"></div>
          <div class="ray ray-2"></div>
          <div class="ray ray-3"></div>
          <div class="ray ray-4"></div>
          <div class="ray ray-5"></div>
          <div class="ray ray-6"></div>
        </div>
        
        <!-- 粒子效果 -->
        <div class="particles">
          <div 
            class="particle" 
            v-for="i in 20" 
            :key="i" 
            :style="getParticleStyle(i)"
          ></div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  const getParticleStyle = (index) => {
    const angle = (index * 18) * (Math.PI / 180)
    const distance = 200 + Math.random() * 100
    const x = Math.cos(angle) * distance
    const y = Math.sin(angle) * distance
    const delay = index * 0.1
    const duration = 3 + Math.random() * 2
    
    return {
      left: `calc(50% + ${x}px)`,
      top: `calc(50% + ${y}px)`,
      animationDelay: `${delay}s`,
      animationDuration: `${duration}s`
    }
  }
  </script>
  
  <style scoped>
  .blackhole-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 0;
    background: #000000;
  }
  
  .blackhole-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 800px;
    height: 800px;
  }
  
  /* 旋转环 */
  .ring {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border: 2px solid;
    border-radius: 50%;
    border-color: rgba(59, 130, 246, 0.3);
    opacity: 0.6;
  }
  
  .ring-1 {
    width: 400px;
    height: 400px;
    animation: rotate 20s linear infinite;
    border-color: rgba(59, 130, 246, 0.2);
  }
  
  .ring-2 {
    width: 500px;
    height: 500px;
    animation: rotate 25s linear infinite reverse;
    border-color: rgba(139, 92, 246, 0.2);
  }
  
  .ring-3 {
    width: 600px;
    height: 600px;
    animation: rotate 30s linear infinite;
    border-color: rgba(59, 130, 246, 0.15);
  }
  
  /* 吸积盘 */
  .accretion-disk {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 350px;
    height: 350px;
    border-radius: 50%;
    overflow: hidden;
  }
  
  .disk-segment {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    opacity: 0.4;
  }
  
  .disk-1 {
    background: conic-gradient(
      from 0deg,
      transparent 0deg,
      rgba(59, 130, 246, 0.3) 45deg,
      rgba(139, 92, 246, 0.4) 90deg,
      rgba(59, 130, 246, 0.3) 135deg,
      transparent 180deg,
      rgba(59, 130, 246, 0.2) 225deg,
      rgba(139, 92, 246, 0.3) 270deg,
      rgba(59, 130, 246, 0.2) 315deg,
      transparent 360deg
    );
    animation: rotate 15s linear infinite;
    clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  }
  
  .disk-2 {
    background: conic-gradient(
      from 90deg,
      transparent 0deg,
      rgba(139, 92, 246, 0.3) 45deg,
      rgba(59, 130, 246, 0.4) 90deg,
      rgba(139, 92, 246, 0.3) 135deg,
      transparent 180deg,
      rgba(139, 92, 246, 0.2) 225deg,
      rgba(59, 130, 246, 0.3) 270deg,
      rgba(139, 92, 246, 0.2) 315deg,
      transparent 360deg
    );
    animation: rotate 18s linear infinite reverse;
    clip-path: polygon(50% 100%, 0% 0%, 100% 0%);
  }
  
  .disk-3 {
    background: conic-gradient(
      from 180deg,
      transparent 0deg,
      rgba(59, 130, 246, 0.2) 45deg,
      rgba(139, 92, 246, 0.3) 90deg,
      rgba(59, 130, 246, 0.2) 135deg,
      transparent 180deg,
      rgba(59, 130, 246, 0.3) 225deg,
      rgba(139, 92, 246, 0.4) 270deg,
      rgba(59, 130, 246, 0.3) 315deg,
      transparent 360deg
    );
    animation: rotate 12s linear infinite;
    clip-path: polygon(0% 50%, 100% 0%, 100% 100%);
  }
  
  .disk-4 {
    background: conic-gradient(
      from 270deg,
      transparent 0deg,
      rgba(139, 92, 246, 0.2) 45deg,
      rgba(59, 130, 246, 0.3) 90deg,
      rgba(139, 92, 246, 0.2) 135deg,
      transparent 180deg,
      rgba(139, 92, 246, 0.3) 225deg,
      rgba(59, 130, 246, 0.4) 270deg,
      rgba(139, 92, 246, 0.3) 315deg,
      transparent 360deg
    );
    animation: rotate 20s linear infinite reverse;
    clip-path: polygon(100% 50%, 0% 0%, 0% 100%);
  }
  
  /* 事件视界（黑洞中心） */
  .event-horizon {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0, 0, 0, 0.8) 0%, #000000 70%);
    box-shadow: 
      inset 0 0 60px rgba(0, 0, 0, 1),
      0 0 40px rgba(0, 0, 0, 0.8),
      0 0 80px rgba(0, 0, 0, 0.6);
    z-index: 10;
  }
  
  .singularity {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #000000;
    box-shadow: 
      inset 0 0 20px rgba(0, 0, 0, 1),
      0 0 30px rgba(0, 0, 0, 1);
    animation: pulse 3s ease-in-out infinite;
  }
  
  /* 光线扭曲效果 */
  .light-rays {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
  }
  
  .ray {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 2px;
    height: 300px;
    background: linear-gradient(
      to bottom,
      transparent,
      rgba(59, 130, 246, 0.3),
      rgba(139, 92, 246, 0.4),
      transparent
    );
    transform-origin: top center;
    opacity: 0.6;
  }
  
  .ray-1 {
    transform: translate(-50%, -50%) rotate(0deg);
    animation: rayRotate 8s linear infinite;
  }
  
  .ray-2 {
    transform: translate(-50%, -50%) rotate(60deg);
    animation: rayRotate 8s linear infinite 1.33s;
  }
  
  .ray-3 {
    transform: translate(-50%, -50%) rotate(120deg);
    animation: rayRotate 8s linear infinite 2.66s;
  }
  
  .ray-4 {
    transform: translate(-50%, -50%) rotate(180deg);
    animation: rayRotate 8s linear infinite 4s;
  }
  
  .ray-5 {
    transform: translate(-50%, -50%) rotate(240deg);
    animation: rayRotate 8s linear infinite 5.33s;
  }
  
  .ray-6 {
    transform: translate(-50%, -50%) rotate(300deg);
    animation: rayRotate 8s linear infinite 6.66s;
  }
  
  /* 粒子效果 */
  .particles {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
  }
  
  .particle {
    position: absolute;
    width: 3px;
    height: 3px;
    background: rgba(59, 130, 246, 0.8);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 6px rgba(59, 130, 246, 0.6);
  }
  
  /* 动画 */
  @keyframes rotate {
    from {
      transform: translate(-50%, -50%) rotate(0deg);
    }
    to {
      transform: translate(-50%, -50%) rotate(360deg);
    }
  }
  
  @keyframes pulse {
    0%, 100% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 1;
    }
    50% {
      transform: translate(-50%, -50%) scale(0.95);
      opacity: 0.8;
    }
  }
  
  @keyframes rayRotate {
    0% {
      transform: translate(-50%, -50%) rotate(var(--start-angle, 0deg));
      opacity: 0.6;
    }
    50% {
      opacity: 0.3;
    }
    100% {
      transform: translate(-50%, -50%) rotate(calc(var(--start-angle, 0deg) + 360deg));
      opacity: 0.6;
    }
  }
  
  @keyframes particleOrbit {
    0% {
      transform: translate(-50%, -50%) rotate(0deg) translateX(200px) rotate(0deg);
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    90% {
      opacity: 1;
    }
    100% {
      transform: translate(-50%, -50%) rotate(360deg) translateX(200px) rotate(-360deg);
      opacity: 0;
    }
  }
  
  .particle {
    animation: particleOrbit linear infinite;
  }
  
  /* 响应式 */
  @media (max-width: 768px) {
    .blackhole-container {
      width: 600px;
      height: 600px;
    }
    
    .ring-1 {
      width: 300px;
      height: 300px;
    }
    
    .ring-2 {
      width: 400px;
      height: 400px;
    }
    
    .ring-3 {
      width: 500px;
      height: 500px;
    }
    
    .accretion-disk {
      width: 280px;
      height: 280px;
    }
    
    .event-horizon {
      width: 100px;
      height: 100px;
    }
  }
  </style>
  
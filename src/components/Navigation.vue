<template>
  <nav class="navigation">
    <div class="nav-header">
      <h2>知识生产工具</h2>
    </div>
    <ul class="nav-menu">
      <li 
        v-for="item in menuItems" 
        :key="item.key"
        :class="{ active: activeTab === item.key }"
        @click="setActiveTab(item.key)"
        class="nav-item"
      >
        {{ item.label }}
      </li>
    </ul>
  </nav>
</template>

<script>
import { ref, defineExpose } from 'vue'

export default {
  name: 'Navigation',
  setup(props, { emit }) {
    const activeTab = ref('images')
    
    const menuItems = [
      {
        key: 'images',
        label: '图片管理'
      },
      {
        key: 'knowledge',
        label: '知识管理'
      }
    ]
    
    const setActiveTab = (tab) => {
      activeTab.value = tab
      emit('tab-change', tab)
    }
    
    defineExpose({
      activeTab
    })
    
    return {
      activeTab,
      menuItems,
      setActiveTab
    }
  }
}
</script>

<style scoped>
.navigation {
  width: 200px;
  background-color: #f5f5f5;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  overflow-y: auto;
  border-right: 1px solid #ddd;
}

.nav-header {
  padding: 20px;
  background-color: #1890ff;
  color: white;
  text-align: center;
}

.nav-header h2 {
  margin: 0;
  font-size: 18px;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  padding: 15px 20px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
  transition: all 0.3s;
}

.nav-item:hover {
  background-color: #e6f7ff;
}

.nav-item.active {
  background-color: #1890ff;
  color: white;
}
</style>
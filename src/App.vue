<script setup>
import ImageManager from './ImageManager.vue'
import KnowledgeManager from './KnowledgeManager.vue'
import Navigation from './components/Navigation.vue'
import { ref, onMounted } from 'vue'

const activeTab = ref('images')

const handleTabChange = (tab) => {
  activeTab.value = tab
}
</script>

<template>
  <div id="app">
    <Navigation @tab-change="handleTabChange" />
    <div class="main-content">
      <ImageManager v-if="activeTab === 'images'" />
      <KnowledgeManager v-if="activeTab === 'knowledge'" />
    </div>
  </div>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
  padding-top: 0;
  display: flex;
}

.main-content {
  flex: 1;
  margin-left: 200px;
  padding: 20px;
}

.tabs {
  display: none;
}

.tabs button {
  padding: 10px 20px;
  margin: 0 5px;
  border: 1px solid #ddd;
  background-color: #f5f5f5;
  cursor: pointer;
  border-radius: 4px;
}

.tabs button.active {
  background-color: #1890ff;
  color: white;
  border-color: #1890ff;
}

.tabs button:hover {
  background-color: #e6f7ff;
}

.tabs button.active:hover {
  background-color: #40a9ff;
}
</style>
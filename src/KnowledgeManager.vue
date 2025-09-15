<template>
  <div class="knowledge-manager">
    <h2>知识管理</h2>
    
    <!-- 知识点列表 -->
    <div class="knowledge-list">
      <h3>知识点列表</h3>
      <div v-if="knowledgePoints.length === 0" class="no-knowledge">
        暂无知识点
      </div>
      <div v-else class="knowledge-grid">
        <div v-for="knowledge in knowledgePoints" :key="knowledge.id" class="knowledge-item">
          <div class="knowledge-content">
            <p>{{ truncateContent(knowledge.content, 100) }}</p>
          </div>
          <div class="knowledge-info">
            <p class="created-at">创建时间: {{ formatTime(knowledge.created_at) }}</p>
            <button @click="viewDetail(knowledge.id)" class="detail-btn">查看详情</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 知识点详情 -->
    <div v-if="selectedKnowledge" class="knowledge-detail">
      <div class="detail-container">
        <h3>知识点详情</h3>
        <div class="detail-content">
          <p>{{ selectedKnowledge.content }}</p>
          <div v-if="selectedKnowledge.image" class="source-image">
            <h4>来源图片</h4>
            <img :src="'http://localhost:5000' + selectedKnowledge.image.url" 
                 :alt="selectedKnowledge.image.original_name"
                 class="image-preview"
                 @error="handleImageError">
            <p>{{ selectedKnowledge.image.original_name }}</p>
          </div>
          <div class="detail-info">
            <p>创建时间: {{ formatTime(selectedKnowledge.created_at) }}</p>
            <p v-if="selectedKnowledge.updated_at">更新时间: {{ formatTime(selectedKnowledge.updated_at) }}</p>
          </div>
          <div class="detail-actions">
            <button @click="closeDetail" class="close-btn">关闭</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { getKnowledgePoints, getKnowledgeDetail } from './utils/api.js'

export default {
  name: 'KnowledgeManager',
  setup() {
    const knowledgePoints = ref([])
    const selectedKnowledge = ref(null)
    
    // 获取知识点列表
    const fetchKnowledgePoints = async () => {
      try {
        knowledgePoints.value = await getKnowledgePoints()
      } catch (error) {
        console.error('获取知识点列表失败:', error)
        alert('获取知识点列表失败: ' + error.message)
      }
    }
    
    // 查看详情
    const viewDetail = async (knowledgeId) => {
      try {
        selectedKnowledge.value = await getKnowledgeDetail(knowledgeId)
      } catch (error) {
        console.error('获取知识点详情失败:', error)
        alert('获取知识点详情失败: ' + error.message)
      }
    }
    
    // 关闭详情
    const closeDetail = () => {
      selectedKnowledge.value = null
    }
    
    // 格式化时间
    const formatTime = (timeString) => {
      if (!timeString) return ''
      const date = new Date(timeString)
      return date.toLocaleString('zh-CN')
    }
    
    // 截断内容
    const truncateContent = (content, length) => {
      if (!content) return ''
      if (content.length <= length) return content
      return content.substring(0, length) + '...'
    }
    
    // 处理图片加载错误
    const handleImageError = (event) => {
      // 不再设置默认图片，保持空白
      event.target.style.display = 'none'
    }
    
    // 组件挂载时获取知识点列表
    onMounted(() => {
      fetchKnowledgePoints()
    })
    
    return {
      knowledgePoints,
      selectedKnowledge,
      viewDetail,
      closeDetail,
      formatTime,
      truncateContent,
      handleImageError
    }
  }
}
</script>

<style scoped>
.knowledge-manager {
  padding: 20px;
}

.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.knowledge-item {
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s;
  background-color: #fff;
}

.knowledge-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.knowledge-content {
  padding: 15px;
  max-height: 150px;
  overflow: hidden;
}

.knowledge-content p {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.knowledge-info {
  padding: 10px 15px;
  background-color: #f5f5f5;
  border-top: 1px solid #ddd;
}

.created-at {
  font-size: 12px;
  color: #666;
  margin: 0 0 10px 0;
}

.detail-btn {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.detail-btn:hover {
  background-color: #40a9ff;
}

.knowledge-detail {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.detail-container {
  background: white;
  border-radius: 4px;
  max-width: 90%;
  max-height: 90%;
  display: flex;
  flex-direction: column;
}

.detail-container h3 {
  padding: 20px 20px 0 20px;
  margin: 0;
}

.detail-content {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.detail-content p {
  white-space: pre-wrap;
  word-break: break-word;
}

.source-image {
  margin: 20px 0;
  text-align: center;
}

.image-preview {
  max-width: 100%;
  max-height: 200px;
  object-fit: contain;
}

.detail-info {
  margin: 15px 0;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.detail-info p {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
}

.detail-actions {
  padding: 0 20px 20px 20px;
  text-align: right;
}

.close-btn {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.close-btn:hover {
  background-color: #ff7875;
}

.no-knowledge {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
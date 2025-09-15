<template>
  <div class="image-manager">
    <h2>图片管理</h2>
    
    <!-- 上传区域 -->
    <div class="upload-section">
      <div class="upload-area" @click="triggerFileSelect">
        <p>点击选择图片文件或拖拽图片到此区域</p>
        <p class="hint">支持 JPG、PNG、GIF 格式，单个文件不超过10MB</p>
      </div>
      <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*" multiple style="display: none;">
      <div class="upload-actions">
        <button @click="uploadImages" :disabled="selectedFiles.length === 0" class="upload-btn">
          上传图片 ({{ selectedFiles.length }})
        </button>
        <button @click="generateKnowledgeFromImages" :disabled="selectedImageIds.length === 0" class="generate-btn">
          生成知识 ({{ selectedImageIds.length }})
        </button>
      </div>
    </div>
    
    <!-- 图片列表 -->
    <div class="images-list">
      <h3>图片列表</h3>
      <div v-if="images.length === 0" class="no-images">
        暂无图片
      </div>
      <div v-else class="image-grid">
        <div v-for="image in images" :key="image.id" class="image-item" 
             :class="{ selected: selectedImageIds.includes(image.id) }">
          <input 
            type="checkbox" 
            :value="image.id" 
            v-model="selectedImageIds" 
            class="image-checkbox"
          >
          <img :src="'http://localhost:5000' + image.url" 
               :alt="image.original_name"
               class="image-thumbnail"
               @error="handleImageError">
          <div class="image-info">
            <p class="image-name">{{ image.original_name }}</p>
            <p class="status">状态: {{ getStatusText(image.status) }}</p>
            <button @click="deleteImageById(image.id)" class="delete-btn">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { getImages, uploadImage, deleteImage, generateKnowledge } from './utils/api.js'

export default {
  name: 'ImageManager',
  setup() {
    const selectedFiles = ref([])
    const images = ref([])
    const fileInput = ref(null)
    const selectedImageIds = ref([])
    const pollingTimer = ref(null)
    
    // 获取图片列表
    const fetchImages = async () => {
      try {
        images.value = await getImages()
      } catch (error) {
        console.error('获取图片列表失败:', error)
        alert('获取图片列表失败: ' + error.message)
      }
    }
    
    // 触发文件选择
    const triggerFileSelect = () => {
      fileInput.value.click()
    }
    
    // 处理文件选择
    const handleFileSelect = (event) => {
      selectedFiles.value = Array.from(event.target.files)
    }
    
    // 上传图片
    const uploadImages = async () => {
      if (selectedFiles.value.length === 0) return
      
      try {
        // 逐个上传文件，避免并发问题
        for (const file of selectedFiles.value) {
          await uploadImage(file)
        }
        
        selectedFiles.value = []
        fileInput.value.value = ''
        await fetchImages() // 重新获取图片列表
        alert('图片上传成功')
      } catch (error) {
        console.error('上传图片失败:', error)
        alert('上传图片失败: ' + error.message)
      }
    }
    
    // 删除图片
    const deleteImageById = async (imageId) => {
      if (!confirm('确定要删除这张图片吗？')) return
      
      try {
        await deleteImage(imageId)
        await fetchImages() // 重新获取图片列表
        // 从选中列表中移除
        const index = selectedImageIds.value.indexOf(imageId)
        if (index > -1) {
          selectedImageIds.value.splice(index, 1)
        }
        alert('图片删除成功')
      } catch (error) {
        console.error('删除图片失败:', error)
        alert('删除图片失败: ' + error.message)
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'uploaded': '已上传',
        'processing': '处理中',
        'completed': '已完成',
        'failed': '失败'
      }
      return statusMap[status] || status
    }
    
    // 生成知识点
    const generateKnowledgeFromImages = async () => {
      if (selectedImageIds.value.length === 0) {
        alert('请先选择图片')
        return
      }
      
      try {
        const result = await generateKnowledge(selectedImageIds.value)
        console.log('知识点生成结果:', result)
        alert('知识点生成请求已提交')
        // 重新获取图片列表以更新状态
        await fetchImages()
        // 清空选择
        selectedImageIds.value = []
      } catch (error) {
        console.error('生成知识点失败:', error)
        alert('生成知识点失败: ' + error.message)
      }
    }
    
    // 轮询图片状态
    const startPolling = () => {
      // 清除已存在的轮询
      if (pollingTimer.value) {
        clearInterval(pollingTimer.value)
      }
      
      // 每5秒轮询一次
      pollingTimer.value = setInterval(async () => {
        // 只有当有图片处于处理中状态时才轮询
        const processingImages = images.value.filter(image => image.status === 'processing')
        if (processingImages.length > 0) {
          await fetchImages()
        }
      }, 5000)
    }
    
    // 处理图片加载错误
    const handleImageError = (event) => {
      // 不再设置默认图片，保持空白
      event.target.style.display = 'none'
    }
    
    // 组件挂载时获取图片列表
    onMounted(() => {
      fetchImages()
      startPolling()
    })
    
    // 组件卸载时清除轮询
    onUnmounted(() => {
      if (pollingTimer.value) {
        clearInterval(pollingTimer.value)
      }
    })
    
    return {
      selectedFiles,
      images,
      fileInput,
      selectedImageIds,
      triggerFileSelect,
      handleFileSelect,
      uploadImages,
      deleteImageById,
      getStatusText,
      generateKnowledgeFromImages,
      handleImageError
    }
  }
}
</script>

<style scoped>
.image-manager {
  padding: 20px;
}

.upload-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px dashed #ccc;
  border-radius: 4px;
  text-align: center;
}

.upload-area {
  padding: 30px;
  border: 2px dashed #1890ff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
}

.upload-area:hover {
  background-color: #e6f7ff;
  border-color: #40a9ff;
}

.upload-area p {
  margin: 0 0 10px 0;
}

.hint {
  font-size: 12px;
  color: #999;
}

.upload-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.upload-btn, .generate-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.upload-btn {
  background-color: #1890ff;
  color: white;
}

.upload-btn:hover:not(:disabled) {
  background-color: #40a9ff;
}

.upload-btn:disabled {
  background-color: #bfbfbf;
  cursor: not-allowed;
}

.generate-btn {
  background-color: #52c41a;
  color: white;
}

.generate-btn:hover:not(:disabled) {
  background-color: #73d13d;
}

.generate-btn:disabled {
  background-color: #bfbfbf;
  cursor: not-allowed;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.image-item {
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  background-color: #fff;
  transition: all 0.3s;
}

.image-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.image-item.selected {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px #1890ff;
}

.image-checkbox {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
  transform: scale(1.3);
}

.image-thumbnail {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.image-info {
  padding: 10px;
}

.image-name {
  font-weight: bold;
  margin: 0 0 5px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status {
  font-size: 14px;
  color: #666;
  margin: 5px 0;
}

.delete-btn {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.delete-btn:hover {
  background-color: #ff7875;
}

.no-images {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
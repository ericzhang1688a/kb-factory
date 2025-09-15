// API工具函数

const API_BASE_URL = 'http://localhost:5000'

// 获取图片列表
export async function getImages() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/images`)
    if (response.ok) {
      return await response.json()
    } else {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  } catch (error) {
    console.error('获取图片列表失败:', error)
    throw error
  }
}

// 上传图片
export async function uploadImage(file) {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch(`${API_BASE_URL}/api/images`, {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      return await response.json()
    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || '上传失败')
    }
  } catch (error) {
    console.error('上传图片失败:', error)
    throw error
  }
}

// 删除图片
export async function deleteImage(imageId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/images/${imageId}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('删除图片失败:', error)
    throw error
  }
}

// 生成知识点
export async function generateKnowledge(imageIds) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/knowledge/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        image_ids: imageIds
      })
    })
    
    if (response.ok) {
      return await response.json()
    } else {
      const errorData = await response.json()
      throw new Error(errorData.error || '生成知识点失败')
    }
  } catch (error) {
    console.error('生成知识点失败:', error)
    throw error
  }
}

// 获取知识点列表
export async function getKnowledgePoints() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/knowledge_points`)
    if (response.ok) {
      return await response.json()
    } else {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  } catch (error) {
    console.error('获取知识点列表失败:', error)
    throw error
  }
}

// 获取知识点详情
export async function getKnowledgeDetail(knowledgeId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/knowledge/${knowledgeId}`)
    if (response.ok) {
      return await response.json()
    } else {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  } catch (error) {
    console.error('获取知识点详情失败:', error)
    throw error
  }
}
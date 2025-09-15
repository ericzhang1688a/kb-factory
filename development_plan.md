# 知识生产工具开发计划

## 技术选型确认

1. 前端：Vue 3 + Vite
2. 后端：Flask (Python)
3. 数据库：MySQL
4. 测试框架：
   - 前端：Vitest + Vue Test Utils
   - 后端：pytest

## 开发模块划分与顺序

### 第一阶段：环境搭建和基础结构
1. 配置开发环境
2. 初始化项目结构
3. 配置测试框架

### 第二阶段：图片管理模块
1. 图片上传功能
2. 图片列表展示
3. 图片删除功能
4. 单元测试

### 第三阶段：知识管理模块
1. 知识点展示
2. 知识点详情查看
3. 单元测试

### 第四阶段：知识生成模块
1. 触发知识提取功能
2. 状态更新和错误处理
3. 单元测试

### 第五阶段：集成和优化
1. 模块集成
2. 界面优化
3. 性能测试

## 详细开发计划

### 1. 环境搭建和基础结构

#### 任务清单：
- 安装并配置后端Flask框架
- 配置数据库连接
- 安装前端测试工具(Vitest)
- 安装后端测试工具(pytest)

#### 测试策略：
- 确保Flask应用能正常启动
- 确保数据库连接正常
- 确保前后端测试框架正常运行

### 2. 图片管理模块

#### 功能实现：
- 实现图片上传API (POST /api/images)
- 实现图片列表API (GET /api/images)
- 实现图片删除API (DELETE /api/images/{id})
- 前端实现图片上传界面
- 前端实现图片列表展示
- 前端实现图片删除功能

#### 数据表结构：
```sql
CREATE TABLE images (
  id INT PRIMARY KEY AUTO_INCREMENT,
  filename VARCHAR(255) NOT NULL, -- UUID文件名
  original_name VARCHAR(255) NOT NULL, -- 原始文件名
  file_path VARCHAR(512) NOT NULL, -- 文件存储路径
  status ENUM('uploaded', 'processing', 'completed', 'failed') DEFAULT 'uploaded',
  knowledge_point_id INT NULL, -- 关联知识点ID
  error_message TEXT NULL, -- 错误信息
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 测试策略：
- 测试上传不同类型和大小的文件
- 测试文件格式验证
- 测试文件列表获取
- 测试删除功能
- 测试边界条件（如大文件、特殊字符文件名等）

### 3. 知识管理模块

#### 功能实现：
- 实现知识点列表API (GET /api/knowledge_points)
- 实现知识点详情API (GET /api/knowledge/{id})
- 前端实现知识点列表展示
- 前端实现知识点详情查看（包括关联的图片）

#### 数据表结构：
```sql
CREATE TABLE knowledge_points (
  id INT PRIMARY KEY AUTO_INCREMENT,
  content TEXT NOT NULL, -- 知识点内容
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 测试策略：
- 测试知识点列表获取
- 测试知识点详情获取
- 测试关联图片的显示
- 测试空数据和异常情况处理

### 4. 知识生成模块

#### 功能实现：
- 实现知识提取API (POST /api/knowledge/generate)
- 实现与Dify API的对接
- 前端实现知识提取触发按钮
- 前端实现实时状态更新

#### 工作流程：
1. 用户选择图片并点击"生成知识"
2. 前端发送选中图片ID列表到后端
3. 后端更新选中图片状态为"processing"
4. 后端调用Dify API处理图片
5. 根据处理结果：
   - 成功：保存知识点到数据库，更新图片状态为"completed"，建立关联关系
   - 失败：更新图片状态为"failed"，记录错误信息
6. 前端轮询或通过WebSocket获取状态更新

#### 测试策略：
- 测试Dify API调用
- 测试状态更新机制
- 测试成功和失败场景
- 测试并发处理场景

### 5. 集成和优化

#### 功能实现：
- 实现导航菜单
- 整体界面优化
- 性能优化
- 错误处理完善

#### 测试策略：
- 端到端测试
- 用户体验测试
- 性能测试
- 安全测试

## 开发原则

1. **模块化开发**：每个模块独立开发和测试，确保功能完整后再进入下一模块
2. **测试先行**：每个功能点都要有对应的单元测试
3. **代码复用**：提取公共组件和工具函数
4. **错误处理**：完善的错误处理和用户提示
5. **安全性**：API密钥安全存储，文件上传验证

## 预期交付物

1. 完整的前后端代码
2. 数据库设计文档
3. API接口文档
4. 测试报告
5. 部署文档
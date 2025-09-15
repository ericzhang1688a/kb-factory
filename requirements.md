# 知识生产工具需求文档 (MVP版本)

## 项目概述

开发一个基于 Vue + Flask + MySQL 的知识生产工具，支持从本地上传图片，调用 Dify 工作流和视觉模型提取知识，存储到数据库，并建立文本知识和图片的关联关系。

MVP目标：实现一个最小可行产品，包含核心功能，可以演示完整的从图片上传到知识提取的工作流程。

## 技术栈

- 前端：Vue 3 (基于Vite)
- 后端：Flask (Python)
- 数据库：MySQL
- AI服务：Dify工作流 + 视觉模型

## 系统配置信息

- Dify请求地址：http://10.110.1.113:8080/v1
- API密钥：app-Yn6WZxVWnvaIra2K2Hui8eDV
- MySQL地址：10.110.1.113:3306
- MySQL用户名：root
- MySQL密码：root
- 文件上传路径：./uploads
- 文件命名策略：使用唯一文件名（UUID）避免冲突

## MVP功能需求

### 前端导航菜单
系统前端应包含左侧导航菜单，菜单项包括：
- 图片管理
- 知识管理

### 1. 图片管理模块 (MVP版本)

- 支持本地图片文件上传（单个或批量）
- 图片格式验证（jpg, png, jpeg）
- 图片大小限制（最大10MB）
- 图片列表展示（包含缩略图）
- 图片状态显示（未处理/处理中/已完成/失败）
- 删除图片功能
- 选择图片并触发知识提取功能

### 2. 知识管理模块 (MVP版本)

- 查看从AI转换过来的知识点列表
- 点击查看源文件可查看该知识来源的图片
- 显示知识点内容
- 显示知识点创建时间

### 3. 知识生成模块 (MVP版本)

- 选择一张或多张图片触发Dify API
- 显示处理状态（处理中/完成/失败）
- 显示处理结果或错误信息

## 数据库设计 (简化版)

### 知识点表 (knowledge_points)
- id: 主键
- content: 文本知识内容
- created_at: 创建时间
- updated_at: 更新时间

### 图片表 (images)
- id: 主键
- filename: 文件名（UUID生成）
- original_name: 原始文件名
- file_path: 文件存储路径
- status: 处理状态 (uploaded, processing, completed, failed)
- knowledge_point_id: 关联的知识点ID
- error_message: 错误信息
- created_at: 创建时间
- updated_at: 更新时间

### 任务记录 (简化为状态更新)
MVP版本中，任务信息将直接记录在图片表中，不单独建立任务表。

## API接口设计 (MVP版本)

### 后端接口

1. 图片管理接口
   - GET /api/images - 获取图片列表
   - POST /api/images - 上传图片
   - DELETE /api/images/{id} - 删除图片

2. 知识生成接口
   - POST /api/knowledge/generate - 触发知识提取
   - GET /api/knowledge/{id} - 获取知识点详情

3. 知识点查询接口
   - GET /api/knowledge_points - 获取知识点列表

## 工作流程 (MVP版本)

1. 用户上传图片到系统
2. 图片保存到服务器并记录到数据库（状态为uploaded）
3. 用户在图片列表中选择一张或多张图片
4. 用户点击"生成知识"按钮触发处理流程
5. 系统更新选中图片状态为processing
6. 系统调用Dify API处理图片
7. 处理完成后，系统:
   - 保存知识点到数据库
   - 更新图片状态为completed或failed
   - 建立图片与知识点的关联关系
8. 用户可以在知识管理页面查看提取的知识点

## 部署要求

- Python环境 (Flask应用)
- Node.js环境 (Vue前端)
- MySQL数据库
- 可访问Dify服务的网络环境

## 安全考虑

- API密钥的安全存储（使用环境变量）
- 文件上传的安全验证
- 数据库访问权限控制
# 知识生产工具 (kb-factory)

一个基于 Vue 3 + Flask + MySQL 的知识生产工具，支持从本地上传图片，调用 Dify 工作流和视觉模型提取知识，存储到数据库，并建立文本知识和图片的关联关系。

## 功能简介

本系统主要包含以下功能模块：

1. 图片管理模块
   - 支持本地图片文件上传（单个或批量）
   - 图片格式验证（jpg, png, gif）
   - 图片列表展示（包含缩略图）
   - 图片状态显示（已上传/处理中/已完成/失败）
   - 删除图片功能
   - 选择图片并触发知识提取功能

2. 知识管理模块
   - 查看从AI转换过来的知识点列表
   - 查看知识点详情及来源图片
   - 显示知识点内容和创建时间

3. 知识生成模块
   - 选择一张或多张图片触发Dify API
   - 显示处理状态和结果

## 技术栈

- 前端：Vue 3 (基于 Vite)
- 后端：Flask (Python)
- 数据库：MySQL
- AI服务：Dify工作流 + 视觉模型

## 目录结构

```
kb-factory/
├── backend/                 # 后端代码
│   ├── app/                 # Flask应用
│   │   ├── api/             # API路由
│   │   └── models/          # 数据模型
│   ├── tests/               # 后端测试
│   ├── config.py            # 配置文件
│   ├── init_db.sql          # 数据库初始化脚本
│   └── run.py               # 后端启动文件
├── src/                     # 前端源码
│   ├── components/          # Vue组件
│   ├── utils/               # 工具函数
│   ├── App.vue              # 主应用组件
│   ├── ImageManager.vue     # 图片管理组件
│   ├── KnowledgeManager.vue # 知识管理组件
│   └── main.js              # 前端入口文件
├── uploads/                 # 上传文件存储目录
├── package.json             # 前端依赖配置
└── requirements.txt         # 后端依赖配置
```

## 部署方式

### 环境要求

- Node.js >= 20.19.0
- Python >= 3.8
- MySQL >= 5.7

### 前端部署

1. 安装依赖：
   ```sh
   npm install
   ```

2. 开发模式运行：
   ```sh
   npm run dev
   ```

3. 生产环境构建：
   ```sh
   npm run build
   ```

### 后端部署

1. 安装Python依赖：
   ```sh
   pip install -r requirements.txt
   ```

2. 配置环境变量：
   - 创建 `.env` 文件，配置 Dify API 密钥等信息
   - 示例：
     ```
     DIFY_API_KEY=your_dify_api_key
     DIFY_API_URL=your_dify_api_url
     ```

3. 初始化数据库：
   - 执行 [init_db.sql](backend/init_db.sql) 脚本创建数据表

4. 运行后端服务：
   ```sh
   python backend/run.py
   ```

### 数据库配置

系统使用 MySQL 数据库，需要配置以下环境变量：
- `MYSQL_HOST`: MySQL 主机地址
- `MYSQL_PORT`: MySQL 端口
- `MYSQL_USER`: MySQL 用户名
- `MYSQL_PASSWORD`: MySQL 密码
- `MYSQL_DATABASE`: 数据库名

### Dify 配置

系统需要配置 Dify 工作流信息：
- `DIFY_API_KEY`: Dify API 密钥
- `DIFY_API_URL`: Dify API 地址

## 开发计划

详见 [development_plan.md](development_plan.md)

## API 文档

详见 [difyapi.md](difyapi.md)
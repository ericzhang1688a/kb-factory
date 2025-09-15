-- 创建数据库
CREATE DATABASE IF NOT EXISTS kb_factory;
USE kb_factory;

-- 创建图片表
CREATE TABLE IF NOT EXISTS images (
  id INT PRIMARY KEY AUTO_INCREMENT,
  filename VARCHAR(255) NOT NULL, -- UUID生成的文件名
  original_name VARCHAR(255) NOT NULL, -- 原始文件名
  file_path VARCHAR(512) NOT NULL, -- 文件存储路径
  status ENUM('uploaded', 'processing', 'completed', 'failed') DEFAULT 'uploaded',
  knowledge_point_id INT NULL, -- 关联知识点ID
  error_message TEXT NULL, -- 错误信息
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建知识点表
CREATE TABLE IF NOT EXISTS knowledge_points (
  id INT PRIMARY KEY AUTO_INCREMENT,
  content TEXT NOT NULL, -- 知识点内容
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入一些测试数据
INSERT INTO images (filename, original_name, file_path, status) VALUES 
('test1.jpg', '测试图片1.jpg', './uploads/test1.jpg', 'uploaded'),
('test2.png', '测试图片2.png', './uploads/test2.png', 'completed');
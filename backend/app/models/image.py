from .. import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # UUID生成的文件名
    original_name = db.Column(db.String(255), nullable=False)  # 原始文件名
    file_path = db.Column(db.String(512), nullable=False)  # 文件存储路径
    status = db.Column(db.Enum('uploaded', 'processing', 'completed', 'failed'), 
                       default='uploaded')
    knowledge_point_id = db.Column(db.Integer, nullable=True)  # 关联知识点ID
    error_message = db.Column(db.Text, nullable=True)  # 错误信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_name': self.original_name,
            'file_path': self.file_path,
            'status': self.status,
            'knowledge_point_id': self.knowledge_point_id,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'url': f'/uploads/{self.filename}'  # 添加URL字段
        }
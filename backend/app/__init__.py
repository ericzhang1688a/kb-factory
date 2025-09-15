from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# 初始化扩展
db = SQLAlchemy()

def create_app(testing=False):
    app = Flask(__name__)
    CORS(app)
    
    # 检查是否在测试环境中
    if testing or app.config.get('TESTING'):
        # 测试环境使用SQLite内存数据库
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        # 生产环境使用MySQL数据库
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@10.110.1.113/kb_factory'
    
    # 使用绝对路径作为上传目录
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    
    # Dify API配置 - 使用本地部署的Dify
    app.config['DIFY_API_KEY'] = os.environ.get('DIFY_API_KEY') or 'app-Yn6WZxVWnvaIra2K2Hui8eDV'
    app.config['DIFY_API_URL'] = os.environ.get('DIFY_API_URL') or 'http://10.110.1.113:8080/v1'
    
    # 初始化扩展
    db.init_app(app)
    
    # 注册蓝图
    from .api import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app
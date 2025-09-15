import sys
import os
import pytest
import tempfile
import io

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.models.image import Image
from app import db

@pytest.fixture
def client():
    # 明确传递testing=True参数
    app = create_app(testing=True)
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            # 确保使用内存数据库进行测试
            db.create_all()
            yield client
            db.drop_all()

def test_upload_image(client):
    """测试上传图片"""
    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    
    response = client.post('/api/images', 
                          data=data, 
                          content_type='multipart/form-data')
    
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['original_name'] == 'test.jpg'
    assert json_data['status'] == 'uploaded'

def test_get_images(client):
    """测试获取图片列表"""
    # 先上传一张图片
    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    
    client.post('/api/images', 
                data=data, 
                content_type='multipart/form-data')
    
    # 获取图片列表
    response = client.get('/api/images')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['original_name'] == 'test.jpg'

def test_delete_image(client):
    """测试删除图片"""
    # 先上传一张图片
    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    
    response = client.post('/api/images', 
                          data=data, 
                          content_type='multipart/form-data')
    
    assert response.status_code == 201
    json_data = response.get_json()
    image_id = json_data['id']
    
    # 删除图片
    response = client.delete(f'/api/images/{image_id}')
    assert response.status_code == 200
    
    # 确认图片已被删除
    response = client.get('/api/images')
    json_data = response.get_json()
    assert len(json_data) == 0
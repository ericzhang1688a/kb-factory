import sys
import os
import pytest
import io
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.models.image import Image
from app.models.knowledge_point import KnowledgePoint
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

def test_get_knowledge_points_empty(client):
    """测试获取空知识点列表"""
    response = client.get('/api/knowledge_points')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) == 0

def test_get_knowledge_points(client):
    """测试获取知识点列表"""
    # 先创建一些知识点
    kp1 = KnowledgePoint(content="知识点1")
    kp2 = KnowledgePoint(content="知识点2")
    db.session.add_all([kp1, kp2])
    db.session.commit()
    
    response = client.get('/api/knowledge_points')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) == 2
    assert json_data[0]['content'] in ["知识点1", "知识点2"]
    assert json_data[1]['content'] in ["知识点1", "知识点2"]

def test_get_knowledge_detail(client):
    """测试获取知识点详情"""
    # 先创建一个知识点
    kp = KnowledgePoint(content="测试知识点")
    db.session.add(kp)
    db.session.commit()
    
    response = client.get(f'/api/knowledge/{kp.id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['content'] == "测试知识点"
    assert json_data['id'] == kp.id

def test_get_knowledge_detail_not_found(client):
    """测试获取不存在的知识点详情"""
    response = client.get('/api/knowledge/999')
    assert response.status_code == 404

def test_generate_knowledge(client):
    """测试生成知识点"""
    # 先上传一张图片
    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    
    response = client.post('/api/images', 
                          data=data, 
                          content_type='multipart/form-data')
    
    assert response.status_code == 201
    image_data = response.get_json()
    image_id = image_data['id']
    
    # 生成知识点
    generate_data = {
        'image_ids': [image_id]
    }
    
    response = client.post('/api/knowledge/generate',
                          data=json.dumps(generate_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == '知识点生成完成'
    
    # 检查知识点是否创建成功
    response = client.get('/api/knowledge_points')
    assert response.status_code == 200
    knowledge_points = response.get_json()
    assert len(knowledge_points) == 1
    
    # 检查图片状态是否更新
    response = client.get('/api/images')
    assert response.status_code == 200
    images = response.get_json()
    assert len(images) == 1
    assert images[0]['status'] == 'completed'
    assert images[0]['knowledge_point_id'] is not None
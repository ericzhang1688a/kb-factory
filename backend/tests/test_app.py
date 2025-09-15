import sys
import os
import pytest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_backend_is_running(client):
    """测试后端是否正常运行"""
    rv = client.get('/api/test')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['status'] == 'success'
    assert 'Backend is running' in json_data['message']
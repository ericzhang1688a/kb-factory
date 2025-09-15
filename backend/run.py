import sys
import os

# 将app目录添加到Python路径中
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app

# 以开发模式运行应用
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
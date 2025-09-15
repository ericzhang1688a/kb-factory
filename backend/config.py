import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Config:
    # Dify API配置
    DIFY_API_KEY = os.environ.get('DIFY_API_KEY') or 'app-Yn6WZxVWnvaIra2K2Hui8eDV'
    DIFY_API_URL = os.environ.get('DIFY_API_URL') or 'https://api.dify.ai/v1'
    
    # 其他配置项可以在这里添加
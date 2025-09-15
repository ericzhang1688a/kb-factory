import os
import uuid
import requests
import time
import traceback
from flask import jsonify, request, current_app, send_from_directory
from werkzeug.utils import secure_filename
from ..models.image import Image
from ..models.knowledge_point import KnowledgePoint
from .. import db
from . import main

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Dify API配置
DIFY_API_URL = 'http://10.110.1.113:8080/v1'
DIFY_API_KEY = 'app-Yn6WZxVWnvaIra2K2Hui8eDV'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/api/test', methods=['GET'])
def test_connection():
    """
    测试API连接
    """
    return jsonify({
        "status": "success",
        "message": "Backend is running"
    }), 200

@main.route('/api/images', methods=['GET'])
def get_images():
    """
    获取图片列表
    """
    images = Image.query.all()
    images_data = []
    for image in images:
        image_dict = image.to_dict()
        # 确保URL使用正斜杠
        image_dict['url'] = image_dict['url'].replace('\\', '/')
        images_data.append(image_dict)
    return jsonify(images_data), 200

@main.route('/api/images', methods=['POST'])
def upload_image():
    """
    上传图片
    """
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400
    
    file = request.files['file']
    
    # 检查文件名
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    # 检查文件类型
    if file and allowed_file(file.filename):
        # 生成唯一文件名
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = str(uuid.uuid4()) + '.' + file_extension
        
        # 确保上传目录存在
        upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # 保存文件
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # 验证文件是否保存成功
        if not os.path.exists(file_path):
            db.session.rollback()  # 回滚数据库事务
            return jsonify({'error': '文件保存失败'}), 500
        
        # 保存到数据库，确保路径使用正斜杠，状态使用合法值
        image = Image(
            filename=unique_filename,
            original_name=original_filename,
            file_path=file_path.replace('\\', '/'),
            status='uploaded'  # 明确设置状态为合法值
        )
        db.session.add(image)
        db.session.commit()
        
        # 返回图片信息，包括URL
        image_dict = image.to_dict()
        image_dict['url'] = f'/uploads/{unique_filename}'
        return jsonify(image_dict), 201
    else:
        return jsonify({'error': '不支持的文件类型'}), 400

@main.route('/api/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """
    删除图片
    """
    image = Image.query.get_or_404(image_id)
    
    # 从文件系统中删除文件
    if os.path.exists(image.file_path):
        os.remove(image.file_path)
    
    # 从数据库中删除记录
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({'message': '图片删除成功'}), 200

@main.route('/api/knowledge_points', methods=['GET'])
def get_knowledge_points():
    """
    获取知识点列表
    """
    knowledge_points = KnowledgePoint.query.all()
    return jsonify([kp.to_dict() for kp in knowledge_points]), 200

@main.route('/api/knowledge/<int:knowledge_id>', methods=['GET'])
def get_knowledge_detail(knowledge_id):
    """
    获取知识点详情
    """
    knowledge_point = KnowledgePoint.query.get_or_404(knowledge_id)
    # 获取关联的图片
    image = Image.query.filter_by(knowledge_point_id=knowledge_id).first()
    
    result = knowledge_point.to_dict()
    if image:
        result['image'] = image.to_dict()
    
    return jsonify(result), 200

@main.route('/api/knowledge/generate', methods=['POST'])
def generate_knowledge():
    """
    生成知识点
    """
    print("=" * 50)
    print("开始处理知识点生成请求")
    print("=" * 50)
    
    data = request.get_json()
    print(f"接收到的请求数据: {data}")
    
    image_ids = data.get('image_ids', [])
    print(f"需要处理的图片ID列表: {image_ids}")
    
    if not image_ids:
        print("错误: 未选择图片")
        return jsonify({'error': '未选择图片'}), 400
    
    # 从应用配置中获取Dify API配置
    DIFY_API_KEY = current_app.config.get('DIFY_API_KEY')
    DIFY_API_URL = current_app.config.get('DIFY_API_URL', 'http://10.110.1.113:8080/v1')
    
    print(f"Dify API配置 - URL: {DIFY_API_URL}, API_KEY是否存在: {bool(DIFY_API_KEY)}")
    
    if not DIFY_API_KEY:
        print("错误: DIFY_API_KEY 未设置")
        return jsonify({'error': 'DIFY_API_KEY 未设置'}), 500
    
    generated_knowledge = []
    
    # 处理每张图片
    for image_id in image_ids:
        print(f"\n--- 开始处理图片 ID: {image_id} ---")
        image = Image.query.get(image_id)
        if not image:
            print(f"警告: 图片 ID {image_id} 不存在，跳过处理")
            continue
            
        # 更新图片状态为处理中
        print(f"更新图片 {image_id} 状态为 'processing'")
        image.status = 'processing'
        db.session.commit()
        
        try:
            # 构建图片访问URL
            # 使用实际IP地址而不是localhost，确保Dify可以访问
            host = request.host.split(':')[0]  # 获取主机地址部分
            if host == 'localhost' or host == '127.0.0.1':
                # 如果是本地地址，需要替换为实际IP地址
                # 假设后端服务运行在10.110.1.245（根据difyapidemo.py中的示例）
                image_url = f"http://10.110.1.245:5000/uploads/{image.filename}"
            else:
                image_url = f"{request.url_root}uploads/{image.filename}"
            print(f"构建图片访问URL: {image_url}")
            
            # 验证图片URL是否可访问
            print("验证图片URL可访问性...")
            try:
                verify_response = requests.get(image_url, timeout=10)
                print(f"图片URL访问测试 - 状态码: {verify_response.status_code}, 内容长度: {len(verify_response.content)} 字节")
                if verify_response.status_code != 200:
                    print(f"警告: 图片URL访问异常，状态码: {verify_response.status_code}")
            except Exception as verify_error:
                print(f"警告: 图片URL访问测试失败: {verify_error}")
            
            # 调用Dify工作流，使用远程URL方式
            workflow_headers = {
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # 根据API文档，将远程图片URL添加到inputs参数中
            workflow_data = {
                "inputs": {
                    "images": [{                    
                        "transfer_method": "remote_url",
                        "url": image_url,
                        "type": "image"
                    }]
                },
                "response_mode": "blocking",
                "user": "kb-factory-user"
            }
            
            print(f"准备发送到Dify的请求数据:")
            print(f"  URL: {DIFY_API_URL}/workflows/run")
            print(f"  Headers: {workflow_headers}")
            print(f"  Data: {workflow_data}")
            
            print("开始调用Dify工作流...")
            workflow_response = requests.post(
                f'{DIFY_API_URL}/workflows/run',
                headers=workflow_headers,
                json=workflow_data,
                timeout=100  # 根据difyapi.md中提到的Cloudflare 100秒超时限制设置
            )
            
            print(f"Dify响应详情:")
            print(f"  状态码: {workflow_response.status_code}")
            print(f"  响应头: {dict(workflow_response.headers)}")
            print(f"  响应内容: {workflow_response.text}")
            
            # 根据difyapi.md文档，检查响应状态码和内容
            if workflow_response.status_code in [200, 201]:
                try:
                    result = workflow_response.json()
                    print(f"Dify完整响应JSON: {result}")
                    
                    # 从Dify响应中提取知识点内容
                    # 根据difyapi.md文档，blocking模式返回CompletionResponse对象
                    outputs = result.get('data', {}).get('outputs', {})
                    print(f"从响应中提取的outputs: {outputs}")
                    
                    knowledge_content = outputs.get('knowledge', '') if outputs else ''
                    print(f"提取到的知识点内容: {knowledge_content}")
                    
                    # 如果没有获取到知识点内容，尝试其他可能的字段
                    if not knowledge_content:
                        print("未找到'knowledge'字段，尝试查找其他可能的输出字段...")
                        # 尝试获取其他可能的输出字段
                        for key, value in outputs.items():
                            if isinstance(value, str) and len(value) > 0:
                                knowledge_content = value
                                print(f"使用字段 '{key}' 的内容作为知识点: {knowledge_content}")
                                break
                    
                    if not knowledge_content:
                        knowledge_content = "未能从图片中提取到知识点内容"
                        print("未能提取到有效知识点内容")
                    
                    # 保存知识点到数据库
                    print("保存知识点到数据库...")
                    knowledge_point = KnowledgePoint(content=knowledge_content)
                    db.session.add(knowledge_point)
                    db.session.flush()  # 获取knowledge_point的ID
                    print(f"知识点保存成功，ID: {knowledge_point.id}")
                    
                    # 更新图片状态为完成，并关联知识点
                    image.status = 'completed'
                    image.knowledge_point_id = knowledge_point.id
                    db.session.commit()
                    print(f"图片 {image_id} 状态更新为 'completed'，关联知识点ID: {knowledge_point.id}")
                    
                    generated_knowledge.append({
                        'image_id': image.id,
                        'knowledge_id': knowledge_point.id,
                        'status': 'success'
                    })
                    print(f"图片 {image_id} 处理完成")
                except Exception as json_error:
                    print(f"解析Dify响应JSON时出错: {json_error}")
                    raise
            else:
                # 更新图片状态为失败
                error_msg = f'Dify工作流调用失败: {workflow_response.status_code} - {workflow_response.text}'
                print(f"错误: {error_msg}")
                image.status = 'failed'
                image.error_message = error_msg
                db.session.commit()
                print(f"图片 {image_id} 状态更新为 'failed'")
                
                generated_knowledge.append({
                    'image_id': image.id,
                    'status': 'failed',
                    'error': error_msg
                })
            
        except requests.exceptions.Timeout:
            error_msg = 'Dify工作流调用超时(100秒)'
            print(f"错误: {error_msg}")
            image.status = 'failed'
            image.error_message = error_msg
            db.session.commit()
            generated_knowledge.append({
                'image_id': image.id,
                'status': 'failed',
                'error': error_msg
            })
            
        except requests.exceptions.ConnectionError as conn_error:
            error_msg = f'Dify工作流连接错误: {str(conn_error)}'
            print(f"连接错误: {error_msg}")
            image.status = 'failed'
            image.error_message = error_msg
            db.session.commit()
            generated_knowledge.append({
                'image_id': image.id,
                'status': 'failed',
                'error': error_msg
            })
            
        except Exception as e:
            # 更新图片状态为失败
            error_msg = str(e)
            print(f"处理图片 {image_id} 时发生未预期错误: {error_msg}")
            print(f"错误详情: {traceback.format_exc()}")
            image.status = 'failed'
            image.error_message = error_msg
            db.session.commit()
            
            generated_knowledge.append({
                'image_id': image.id,
                'status': 'failed',
                'error': error_msg
            })
        finally:
            print(f"--- 图片 ID {image_id} 处理结束 ---\n")
    
    print("=" * 50)
    print("知识点生成请求处理完成")
    print("=" * 50)
    
    return jsonify({
        'message': '知识点生成完成',
        'results': generated_knowledge
    }), 200

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    访问上传的文件
    """
    upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
    # 构建正确的文件路径
    file_path = os.path.join(upload_folder, filename)
    
    # 确保文件存在
    if os.path.exists(file_path):
        return send_from_directory(upload_folder, filename)
    else:
        # 返回404
        return jsonify({'error': '文件未找到'}), 404

@main.route('/placeholder.png')
def placeholder_image():
    """
    返回占位图
    """
    # 创建一个简单的1x1像素的透明PNG图片
    placeholder = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    return placeholder, 200, {'Content-Type': 'image/png'}
import requests
import json

# Dify API配置
API_KEY = "app-Yn6WZxVWnvaIra2K2Hui8eDV"
API_BASE_URL = "http://10.110.1.113:8080/v1"
WORKFLOW_RUN_URL = f"{API_BASE_URL}/workflows/run"
FILE_UPLOAD_URL = f"{API_BASE_URL}/files/upload"

def upload_file(file_path, user):
    """
    上传文件到Dify
    """
    url = FILE_UPLOAD_URL
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }

    try:
        print("上传文件中...")
        with open(file_path, 'rb') as file:
            files = {
                'file': (file_path, file, 'image/jpeg')
            }
            data = {
                "user": user,
                "type": "image"  # 设置文件类型为image
            }

            response = requests.post(url, headers=headers, files=files, data=data)
            if response.status_code == 201:  # 201 表示创建成功
                print("文件上传成功")
                return response.json().get("id")  # 获取上传的文件 ID
            else:
                print(f"文件上传失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

def run_workflow_with_remote_image(image_url, user, response_mode="blocking"):
    """
    运行工作流，将远程图片URL作为输入参数
    """
    url = WORKFLOW_RUN_URL
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 根据API文档，将远程图片URL添加到inputs参数中
    data = {
        "inputs": {
            "images": [{                    # 使用images字段
                "transfer_method": "remote_url",
                "url": image_url,
                "type": "image"
            }]
        },
        "response_mode": response_mode,
        "user": user
    }

    try:
        print("运行工作流...")
        response = requests.post(url, headers=headers, json=data)
        print(f"工作流响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("工作流执行成功")
            return response.json()
        else:
            print(f"工作流执行失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return {"status": "error", "message": f"Failed to execute workflow, status code: {response.status_code}"}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}

def run_workflow(file_id, user, response_mode="blocking"):
    """
    运行工作流，将上传的文件作为输入参数
    """
    url = WORKFLOW_RUN_URL
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 根据API文档，将文件添加到inputs参数中
    data = {
        "inputs": {
            "images": [{                    # 根据需求，使用images字段
                "transfer_method": "local_file",
                "upload_file_id": file_id,
                "type": "image"
            }]
        },
        "response_mode": response_mode,
        "user": user
    }

    try:
        print("运行工作流...")
        response = requests.post(url, headers=headers, json=data)
        print(f"工作流响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("工作流执行成功")
            return response.json()
        else:
            print(f"工作流执行失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return {"status": "error", "message": f"Failed to execute workflow, status code: {response.status_code}"}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}

def main():
    """
    主函数
    """
    user = "test-user"
    
    # 使用远程图片URL
    image_url = "http://10.110.1.245:5000/uploads/951b99b5-e43f-469c-8f39-6154c51946cb.png"
    
    print(f"使用远程图片: {image_url}")
    result = run_workflow_with_remote_image(image_url, user)
    print("工作流执行结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 如果您还想测试本地文件上传方式，可以取消下面代码的注释
    '''
    file_path = "test.jpeg"
    # 上传文件
    file_id = upload_file(file_path, user)
    
    if file_id:
        print(f"获取到文件ID: {file_id}")
        # 文件上传成功，继续运行工作流
        result = run_workflow(file_id, user)
        print("工作流执行结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("文件上传失败，无法执行工作流")
    '''

if __name__ == "__main__":
    main()
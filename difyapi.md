inputs (object) Required 允许传入 App 定义的各变量值。 inputs 参数包含了多组键值对（Key/Value pairs），每组的键对应一个特定变量，每组的值则是该变量的具体值。变量可以是文件列表类型。 文件列表类型变量适用于传入文件结合文本理解并回答问题，仅当模型支持该类型文件解析能力时可用。如果该变量是文件列表类型，该变量对应的值应是列表格式，其中每个元素应包含以下内容：
type (string) 支持类型：
document 具体类型包含：'TXT', 'MD', 'MARKDOWN', 'PDF', 'HTML', 'XLSX', 'XLS', 'DOCX', 'CSV', 'EML', 'MSG', 'PPTX', 'PPT', 'XML', 'EPUB'
image 具体类型包含：'JPG', 'JPEG', 'PNG', 'GIF', 'WEBP', 'SVG'
audio 具体类型包含：'MP3', 'M4A', 'WAV', 'WEBM', 'AMR'
video 具体类型包含：'MP4', 'MOV', 'MPEG', 'MPGA'
custom 具体类型包含：其他文件类型
transfer_method (string) 传递方式，remote_url 图片地址 / local_file 上传文件
url (string) 图片地址（仅当传递方式为 remote_url 时）
upload_file_id (string) 上传文件 ID（仅当传递方式为 local_file 时）
response_mode (string) Required 返回响应模式，支持：
streaming 流式模式（推荐）。基于 SSE（Server-Sent Events）实现类似打字机输出方式的流式返回。
blocking 阻塞模式，等待执行完毕后返回结果。（请求若流程较长可能会被中断）。 由于 Cloudflare 限制，请求会在 100 秒超时无返回后中断。
user (string) Required 用户标识，用于定义终端用户的身份，方便检索、统计。 由开发者定义规则，需保证用户标识在应用内唯一。API 无法访问 WebApp 创建的会话。
files (array[object]) 可选
trace_id (string) Optional 链路追踪ID。适用于与业务系统已有的trace组件打通，实现端到端分布式追踪等场景。如果未指定，系统将自动生成 trace_id。支持以下三种方式传递，具体优先级依次为：
Header：推荐通过 HTTP Header X-Trace-Id 传递，优先级最高。
Query 参数：通过 URL 查询参数 trace_id 传递。
Request Body：通过请求体字段 trace_id 传递（即本字段）。
Response
当 response_mode 为 blocking 时，返回 CompletionResponse object。 当 response_mode 为 streaming时，返回 ChunkCompletionResponse object 流式序列。

CompletionResponse
返回完整的 App 结果，Content-Type 为 application/json 。

workflow_run_id (string) workflow 执行 ID
task_id (string) 任务 ID，用于请求跟踪和下方的停止响应接口
data (object) 详细内容
id (string) workflow 执行 ID
workflow_id (string) 关联 Workflow ID
status (string) 执行状态, running / succeeded / failed / stopped
outputs (json) Optional 输出内容
error (string) Optional 错误原因
elapsed_time (float) Optional 耗时(s)
total_tokens (int) Optional 总使用 tokens
total_steps (int) 总步数（冗余），默认 0
created_at (timestamp) 开始时间
finished_at (timestamp) 结束时间

# Request
curl -X POST 'http://10.110.1.113:8080/v1/workflows/run' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {},
  "response_mode": "streaming",
  "user": "abc-123"
}'


# Example: file array as an input variabl

{
  "inputs": {
    "{variable_name}":
    [
      {
      "transfer_method": "local_file",
      "upload_file_id": "{upload_file_id}",
      "type": "{document_type}"
      }
    ]
  }
}

#  File upload sample code


import requests
import json

def upload_file(file_path, user):
    upload_url = "https://api.dify.ai/v1/files/upload"
    headers = {
        "Authorization": "Bearer app-xxxxxxxx",
    }

    try:
        print("上传文件中...")
        with open(file_path, 'rb') as file:
            files = {
                'file': (file_path, file, 'text/plain')  # 确保文件以适当的MIME类型上传
            }
            data = {
                "user": user,
                "type": "TXT"  # 设置文件类型为TXT
            }

            response = requests.post(upload_url, headers=headers, files=files, data=data)
            if response.status_code == 201:  # 201 表示创建成功
                print("文件上传成功")
                return response.json().get("id")  # 获取上传的文件 ID
            else:
                print(f"文件上传失败，状态码: {response.status_code}")
                return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

def run_workflow(file_id, user, response_mode="blocking"):
    workflow_url = "https://api.dify.ai/v1/workflows/run"
    headers = {
        "Authorization": "Bearer app-xxxxxxxxx",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": {
            "orig_mail": [{
                "transfer_method": "local_file",
                "upload_file_id": file_id,
                "type": "document"
            }]
        },
        "response_mode": response_mode,
        "user": user
    }

    try:
        print("运行工作流...")
        response = requests.post(workflow_url, headers=headers, json=data)
        if response.status_code == 200:
            print("工作流执行成功")
            return response.json()
        else:
            print(f"工作流执行失败，状态码: {response.status_code}")
            return {"status": "error", "message": f"Failed to execute workflow, status code: {response.status_code}"}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}

# 使用示例
file_path = "{your_file_path}"
user = "difyuser"

# 上传文件
file_id = upload_file(file_path, user)
if file_id:
    # 文件上传成功，继续运行工作流
    result = run_workflow(file_id, user)
    print(result)
else:
    print("文件上传失败，无法执行工作流")


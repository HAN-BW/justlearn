import requests
import time
import threading
import json

# 配置参数
num_requests = 5
concurrent_threads = 5

# 存储结果
results = []


# 发送请求并记录结果的函数
def send_request():
    try:
        start_time = time.time()
        # host = "https://openai.hrlyit.com/"
        host = "https://lls-gpt-westus3.openai.azure.com/"
        url = f"{host}openai/deployments/lls-gpt-4o/chat/completions?api-version=2024-05-01-preview"
        payload = json.dumps({
            "model": "lls-gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": "1+1=？"
                }
            ],
            "stream": True,
            "max_tokens": 5
        })
        headers = {
            'api-key': '6fdef45fa03547898e7943631571850b',
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        end_time = time.time()
        result = {
            "status_code": response.status_code,
            "response_time": end_time - start_time,
            "content": response.text
        }
        results.append(result)
    except Exception as e:
        results.append({"error": str(e)})


# 创建线程并发执行请求
threads = []
for _ in range(num_requests):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    if len(threads) == concurrent_threads:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        threads = []

# 启动剩余的线程
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

# 保存结果到文件
with open("ab_test_results.json", "w") as file:
    json.dump(results, file, indent=4)

print(f"AB 测试完成，结果已保存到 'ab_test_results.json'")

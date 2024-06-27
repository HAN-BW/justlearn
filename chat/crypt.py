import base64
import time

# 示例Base64编码字符串
encoded_str = "SGVsbG8sIHdvcmxkIQ=="

# 记录开始时间
start_time = time.time()

# 执行Base64解码
decoded_bytes = base64.b64decode(encoded_str)

# 记录结束时间
end_time = time.time()

# 计算耗时
elapsed_time = end_time - start_time

# 打印解码后的结果和耗时
decoded_str = decoded_bytes.decode('utf-8')
print(f"Decoded string: {decoded_str}")
print(f"Decoding time: {elapsed_time:.10f} seconds")
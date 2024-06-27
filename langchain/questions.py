import csv
import base64
import json
import tiktoken
import openai
import langchain
import chardet
import langchain_openai
import pymysql
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.vectorstores.docarray import DocArrayInMemorySearch
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma


def output_contents() -> []:
    db = pymysql.connect(
        database="cloudgpt",
        # user="root",
        # password="password",
        # host="10.80.57.91",
        # port=30189
        # user="root",
        # password="123456",
        # host="mysql01.dev.lls.com",
        # port=3860
        user="beecloudplat",
        password="Lls168beecloud!",
        host="10.80.57.218",
        port=23306
    )
    cursor = db.cursor()
    sql = "SELECT content,encoded FROM message_models where role='user' ORDER BY created_at desc limit 500 offset 2000 "
    cursor.execute(sql)
    content_list = []
    column_names = ["问题列表"]
    with open('data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(column_names)
        for row in cursor:
            if len(str(row[0])) > 20:
                continue
            if row[1] is not None:
                # Check if encoded value is NULL
                content = base64.b64decode(row[0].encode('utf-8')).decode('utf-8')
                content_list.append(content)
                csv_writer.writerow((content,))
            else:
                content_list.append(row[0])
                try:
                    csv_writer.writerow((row[0],))
                except Exception:
                    print("error")
    db.close()
    print(content_list)
    return content_list


def get_topics(content_list: []):
    base_url = "https://api.chatanywhere.com.cn/v1"
    api_key = "sk-GLY3ssoPHhx6IOKcBGpPTcMkVAO3LjHWAywCXCcFgn1dyhe0"
    embedding = langchain_openai.OpenAIEmbeddings(
        base_url=base_url,
        api_key=api_key)
    # docsearch = Chroma.from_texts(content_list, embedding)
    vector_db = DocArrayInMemorySearch.from_texts(content_list, embedding)
    retriever = vector_db.as_retriever()

    llm = ChatOpenAI(
        temperature=0.0,
        base_url=base_url,
        api_key=api_key)
    retrieval_qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        verbose=True,
    )
    # retrieval_qa = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     retriever=docsearch,
    #     chain_type="stuff",
    #     verbose=True,
    # )
    stop_word = "stop"
    while True:
        user_input = input("Enter your text (or '" + stop_word + "' to quit): ")
        if user_input.lower() == stop_word:
            print("Exiting the loop...")
            break
        print("You entered:", user_input)
        query = user_input
        result = retrieval_qa.run({"query": query})
        print(result['result'])


def get_topics_by_chat(content_list: []):
    api_key = "sk-GLY3ssoPHhx6IOKcBGpPTcMkVAO3LjHWAywCXCcFgn1dyhe0"
    # base_url = "https://api.chatanywhere.com.cn/v1"
    # model = "gpt-3.5-turbo-1106"
    base_url = "http://172.28.86.42:9000/v1"
    model = "Qwen1.5-7B-Chat"
    messages = [{'role': 'system', 'content': "你是一个整理总结的助手"},
                {'role': 'user', 'content': "我有一个如下的问题汇总文档:" + json.dumps(content_list)},
                {'role': 'user', 'content': "讲这些问题再进一步汇总，给我生成六个使用最多的场景，回答的样式类似：1.代码生成：生成一个java的冒泡排序"}]
    encoding = tiktoken.get_encoding("cl100k_base")
    for row in messages:
        total_tokens = len(encoding.encode(row["content"]))
        print("token数:", total_tokens)

    client = openai.OpenAI(
        base_url=base_url,
        api_key=api_key,
    )

    response = client.chat.completions.create(
        max_tokens=4096,
        model=model,
        messages=messages,
    )
    response_message = response.choices[0].message
    print(response_message)
    print(response_message.content)
    return response_message


input = ['''1. 代码帮助：解决编程语法问题，如"css选择器的使用"，"如何使用CSS进行布局"，"java多线程编程实例"等。
2. 翻译与沟通："Translate to English"和"Translate to Chinese"多次出现，表明用户需要互相翻译内容。
3. SQL查询与错误："SQL \u6309\u7167\u65f6\u95f4\u6392\u5e8f"，"sql like\u8bed\u53e5"等，说明用户可能在数据库操作中有查询问题。
4. 网络请求与错误："curl"命令的使用，"mpc gg20请求错误"等，涉及HTTP/HTTPS请求和网络问题。
5. 安全问题："certification"和"KYC"提及，可能与信息安全认证有关。
6. 系统管理与配置："win10删除文件系统权限"，"Windows AD权限管理"，"MPC GG20设备配置"，这涉及到操作系统和设备管理。


1. 代码生成：使用最多的场景是编程教学和代码示例，如“生成Java的冒泡排序”对应需求“Python的斐波那契数列生成”。
2. 技术文档：很多开发者需要编写或查找API文档，如“requirement research”对应需求“学习MySQL的安装和配置步骤”。
3. 学习资源：针对学习者，比如“Markdown指南”或“Jenkins搭建教程”这类帮助用户提升技能的场景。
4. 错误排查：遇到常见bug，如“nextLinks的使用”或“children渲染问题”，这些都是常见问题库中的高频案例。
5. 翻译服务：提供多语言支持，如“translate to English”适用于各种语言的翻译需求。
6. 自动化工具：如“git clone使用”或“Nginx配置”，这类需求常见于开发者的工作流程中。
1. 代码编辑：要求编写特定功能的代码，如“ISO27001标准解读”对应需求“编写信息安全政策”。
2. 系统运维：涉及系统管理和配置，如“nextLinks的实现原理”或“Kubernetes集群管理”。
3. 项目需求：开发者需要理解并实现功能需求，如“Vue组件注册及使用”对应“在Vue项目中实现数据绑定”。
4. 网络技术：如“SSH密钥验证”或“DNS解析问题”，这类问题在网络环境运行的项目中很常见。
5. 翻译与本地化：适用于产品或文档的多语言优化，如“Chinese字符处理”或“Taiwan产品属于哪个区域”。
6. 安全审计：针对安全需求，如“加密算法验证”或“SQL注入防护”，这类问题在网络安全领域很突出。

1. **代码生成**：
   - 使用场景：Java 编写冒泡排序
   - 问题：生成一个 Java 程序实现冒泡排序
   - 回答：1.1. Java 冒泡排序示例：
   ```java
   public class BubbleSort {
       public static void main(String[] args) {
           int[] array = {5, 2, 9, 1, 5, 6};
           bubbleSort(array);
           for (int num : array) {
               System.out.println(num);
           }
       }

       public static void bubbleSort(int[] arr) {
           int n = arr.length;
           for (int i = 0; i < n - 1; i++) {
               for (int j = 0; j < n - i - 1; j++) {
                   if (arr[j] > arr[j + 1]) {
                       // 交换 arr[j] 和 arr[j+1]
                       int temp = arr[j];
                       arr[j] = arr[j + 1];
                       arr[j + 1] = temp;
                   }
               }
           }
       }
   }
   ```
   
2. **语法咨询**：
   - 使用场景：Markdown 格式问题
   - 问题：如何在 Markdown 中使用`<td>`标签展示布尔值
   - 回答：2.1. 在 Markdown 中表示布尔值 `<td>` 格式：
   ```
   |   | True |
   |---|------|
   | Yes |   √  |
   | No  |   ×  |
   ```

3. **API 使用**：
   - 使用场景：Jenkins 构建脚本
   - 问题：配置 Jenkins 构建项目
   - 回答：3.1. 使用 Jenkins 构建脚本（Groovy）：
   ```groovy
   def build = job('your-project')  
   build.invoke(['build'])
   ```

4. **数据处理**：
   - 使用场景：JSON 解析
   - 问题：将 JSON 转换为 Java 对象
   - 回答：4.1. JSON -> Java 对象示例：
   ```java
   import com.google.gson.Gson;
   String jsonString = "{\"name\":\"John\", \"age\":30}";
   Gson gson = new Gson();
   Person person = gson.fromJson(jsonString, Person.class);
   System.out.println(person.getName()); // 输出: John
   ```

5. **错误排查**：
   - 使用场景：Java 语法错误
   - 问题：如何判断代码中是否有未关闭的括号
   - 回答：5.1. 检查括号是否闭合：
   ```java
   if (condition) {
       // ...
       // 代码块结束时确保有 }
       // 或者使用 Java 8 变量声明式风格
       // (int a = 5) { ... }
   }
   ```

6. **环境配置**：
   - 使用场景：Nginx 重定向
   - 问题：配置 Nginx 重定向请求
   - 回答：6.1. Nginx 重定向配置示例：
   ```
   server {
       location /old-url {
           rewrite ^/old-url /new-url permanent;
       }
   }
   ```

1. **代码生成：** 
   - 1.1. Java冒泡排序
   - 1.2. Nginx配置生成
   - 1.3. Vue.js项目初始化
   - 1.4. Dockerfile的自定义配置
   - 1.5. 英文翻译生成
   - 1.6. SQL查询生成

2. **设置与配置：**
   - 2.1. Nginx服务器配置
   - 2.2. 安装包配置（yum、npmrc）
   - 2.3. Linux系统环境配置
   - 2.4. Nginx 1.20.1部署
   - 2.5. 系统日志设置
   - 2.6. PHP环境配置

3. **错误调试与解决：**
   - 3.1. 报错解析：解析错误代码404
   - 3.2. 错误日志分析
   - 3.3. 语法错误帮助
   - 3.4. 语法错误定位
   - 3.5. 安全审核与漏洞修复
   - 3.6. 报错复现与验证

4. **数据库操作：**
   - 4.1. 数据导入导出
   - 4.2. SQL查询优化
   - 4.3. keytool证书处理
   - 4.4. 数据迁移
   - 4.5. 数据库错误排查
   - 4.6. S3文件上传与下载

5. **系统管理与监控：**
   - 5.1. 安装包检查（yum、yum update）
   - 5.2. 安装与卸载软件
   - 5.3. 安全审计与日志审计
   - 5.4. Centos操作系统更新
   - 5.5. 系统性能监控
   - 5.6. 定期备份策略

6. **编程语言与工具：**
   - 6.1. Vue.js应用开发
   - 6.2. Java语法问题
   - 6.3. AOP编程
   - 6.4. .npmrc文件管理
   - 6.5. Python语法指导
   - 6.6. 其他语言或工具使用问题''']

get_topics_by_chat(input)

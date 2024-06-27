import http.client
import json
import openpyxl
import tiktoken
import openai
from urllib.parse import urlencode
from qwen_agent.llm import get_chat_model
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool


def test():
    conn = http.client.HTTPSConnection("sonar-7.llschain.com")
    payload = ''
    headers = {
        'Cookie': 'Secure'
    }
    url = "/api/rules/search"
    query = {
        "f": "isTemplate,name,lang,langName,severity,status,sysTags,tags,templateKey,actives,params",
        "facets": "languages,types",
        "ps": "200",
        "s": "name",
        "activation": "true",
        "languages": "java",
        "qprofile": "AYpKxU_txqVYNW0noAC0",
    }
    encoded_query_params = urlencode(query)
    # queryStr = "&".join("%s=%s" % (k, v) for k, v in query.items())
    urlStr = url + "?" + encoded_query_params
    conn.request("GET",
                 urlStr,
                 payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    ruleList = json.loads(data)
    output = {}
    if "rules" in ruleList:
        for rule in ruleList['rules']:
            tempURL = "/api/rules/show?actives=true&key=%s" % rule['key']
            conn.request("GET", tempURL, payload, headers)
            tempRes = conn.getresponse()
            if tempRes.status != 200:
                print("Error: %s" % tempRes.status)
                break
            tempData = tempRes.read().decode("utf-8")
            tempRule = json.loads(tempData)
            output[rule['key']] = tempRule['rule']
        else:
            print("No rules found")
    conn.close()
    xlsx = openpyxl.Workbook()
    sheet = xlsx.active
    sheet.title = "SonarQube Rules"
    sheet.append(["Rule Key", "Rule Name", "htmlDesc", "mdDesc", "severity", "status", "lang", "type"])
    for key, value in output.items():
        sheet.append([key, value['name'], value['htmlDesc'], value['mdDesc'],
                      value['severity'], value['status'], value['lang'], value['type']])
    xlsx.save("SonarQubeRules.xlsx")
    print("Done")


def test2():
    encoding = tiktoken.get_encoding("cl100k_base")
    dialogue = [
        "闪烁的星光在夜空中飞舞，\n闪耀的月光照亮了我心中的梦想。\n风吹过大地，带来了凉意，\n让我感受到生活的美好和无尽的可能。\n在这一刻，我感到自己是如此渺小，\n但又如此伟大，因为我拥有奋斗的力量。\n无论前方是什么困难和挑战，\n我都会坚定不移地向前迈进\n直到终于到达梦想的彼岸。",
        "输出一篇200字文章",
        '''春天来了，大自然一派生机盎然的景象。清晨，微风轻轻拂过脸庞，仿佛吹散了冬天的寒冷。满园春色，百花争艳，鲜花盛开，散发出迷人的芬芳。树枝上挂满新绿的嫩叶，鸟儿在枝头欢快地歌唱，仿佛在庆祝春天的到来。

蓝天白云，阳光明媚，透过密密的树叶洒在大地上，让人感受到温暖和希望。小溪潺潺流淌，清澈见底，鱼儿在水中嬉戏，生机勃勃。远处的山峦青翠欲滴，宛如一幅美丽的画卷。春天是生命的开始，是希望的象征，让我们怀着感恩的心情，珍惜每一个春天带来的美好时光。

在这个充满生机和希望的季节里，让我们深呼吸清新的空气，感受大自然的馈赠，让心灵在春风中舒展，让希望在春天中发芽。愿我们在春天里播种爱和善良，收获美好和幸福。愿春天永远留在我们心中，带来希望和温暖。''',
        '''输出一篇200字文章''',
        '''春雨绵绵，柳枝婆娑。滴滴细雨敲击着窗棂，淅沥沥的雨声如一曲轻柔的交响乐，缓缓弥漫在空气中。春雨，是大地的呼吸，是生命的滋润，在雨中，一切都显得那么清新、那么生动。

湿润的土地散发着芳香，小草抬头迎风摇曳，树叶上挂满晶莹的雨珠，如同一颗颗珍珠闪闪发光。远处的山峦笼罩在薄雾中，犹如仙境一般神秘动人。

春雨，是大自然的礼物，是一种神奇的力量，让万物萌发生长，让世界焕发出勃勃生机。在雨中散步，感受雨水滋润心灵，让人心情舒畅愉悦。

愿春雨润物无声，愿生命在春雨中茁壮成长，愿我们珍惜每一个春雨洗礼过的清晨，感悟生命中的美好与希望。让我们与春雨共舞，与大自然共存，感受生命的奇妙和宽广。''',
        '''我的第一个请求是？''',
        '''您的第一个请求是输出一篇100字诗歌。接下来，您可以提出其他问题或请求，我会尽力帮助您。如果有任何需要，请随时告诉我。感谢您使用我的服务！''',
        '''您的第一个请求是输出一篇100字诗歌。以下是我为您创作的诗歌：

在湛蓝的天空下
飘着丝丝白云
微风拂面，轻轻吟唱
花儿绽放，香气袭人
春天来了，带来温暖
大地沐浴在阳光下
生命如梦，短暂而美丽
让我们珍惜，感恩这一切
让爱与希望，永远伴随着我们
让我们在这个春天里
把握每一个美好瞬间。''',
        '''您的第一个请求是输出一篇100字诗歌，以下是为您提供的诗歌：

在湛蓝的天空下
飘着丝丝白云
微风拂面，轻轻吟唱
花儿绽放，香气袭人
春天来了，带来温暖
大地沐浴在阳光下
生命如梦，短暂而美丽
让我们珍惜，感恩这一切
让爱与希望，永远伴随着我们
让我们在这个春天里
把握每一个美好瞬间。''',
        '''您的第一个请求是要求我输出一篇100字诗歌。您有其他需要我帮助的吗？''',
        '''输出一篇200字的文章''',
        '''春天来了，大自然一派生机盎然的景象。清晨，微风轻轻拂过脸庞，仿佛吹散了冬天的寒冷。满园春色，百花争艳，鲜花盛开，散发出迷人的芬芳。树枝上挂满新绿的嫩叶，鸟儿在枝头欢快地歌唱，仿佛在庆祝春天的到来。

蓝天白云，阳光明媚，透过密密的树叶洒在大地上，让人感受到温暖和希望。小溪潺潺流淌，清澈见底，鱼儿在水中嬉戏，生机勃勃。远处的山峦青翠欲滴，宛如一幅美丽的画卷。春天是生命的开始，是希望的象征，让我们怀着感恩的心情，珍惜每一个春天带来的美好时光。

在这个充满生机和希望的季节里，让我们深呼吸清新的空气，感受大自然的馈赠，让心灵在春风中舒展，让希望在春天中发芽。愿我们在春天里播种爱和善良，收获美好和幸福。愿春天永远留在我们心中，带来希望和温暖。''',
        '''世界是一个充满奇迹和可能性的地方，每一天都充满了未知和挑战，也蕴藏着无限的机遇和希望。我们生活在这个多姿多彩的世界里，每一个人都是独一无二的存在，每一个人都有自己的故事和梦想。

在这个喧嚣的社会中，我们常常被琐事与压力所困扰，但不要忘记自己内心的那份初衷和梦想。无论前方是什么困难和挑战，我们都要勇敢地面对，坚定地走下去。因为只有拥有坚定的信念和不屈的意志，我们才能超越自我，创造属于自己的奇迹。

相信自己，相信未来，让我们一起努力向前，尽情展现自己的光芒。生命太短暂，让我们珍惜当下，追逐梦想，活出精彩。愿每一个人都能在这个世界找到自己的位置，活出自己想要的精彩人生。''',
        '''写一篇200字文章''',
        '''生命是一场奇妙的旅程，我们每个人都在这个旅程中扮演着独特的角色。有时我们会遇到风雨，有时我们会迷失方向，但正是这些经历塑造了我们的坚韧和智慧。

在人生的舞台上，我们要学会接受挑战、面对困难，并从中收获成长。困难是暂时的，坚持是必要的。当我们坚定信念，超越恐惧，我们就能够开拓新的领域，追寻更广阔的未来。

与此同时，我们也要懂得感恩和珍惜。感恩我们所拥有的，无论是亲情、友情还是爱情。珍惜每一个瞬间，每一次相聚，每一次微笑。因为生命短暂，而我们拥有的每一刻都值得被珍惜。

与人为善、积极向上，用爱心和善意与他人相处。用自己的力量点亮他人的生活，成就更美好的世界。

在这个多姿多彩的世界里，我们是平凡而不平庸的存在。让我们用热情去拥抱生活，用勇气去挑战自我。相信自己的力量，追逐梦想，活出自己想要的精彩人生。''',
        '''目前有多少上下文''',
        '''在我们当前的对话中，我们共有3个上下文。第一个是关于您要求输出一篇100字诗歌的请求，第二个是关于您想要输出一篇200字的文章的请求，第三个是关于最后一次请求输出一篇200字文章的请求。希望这能帮到您，如果您还有其他问题，请随时告诉我。''',
        '''目前，上下文处于单一上下文环境中，即与您当前的对话。不过，每个对话都是独立的，即使您与我进行多个对话，它们也是彼此分离的上下文。在每个对话中，我会根据您的最新请求来提供相关的回复和帮助。如果您要继续之前的对话，请提供相关问题或请求，并让我知道具体的上下文内容，我将会在您提供的上下文中进行回应。''',
        '''当前上下文是指与与上一个输入相关的信息和提问历史。目前，有两个上下文。

第一个上下文是您的第一个请求，要求输出一篇100字诗歌。

第二个上下文是您的第二个请求，要求输出一篇200字的文章。

如果您有任何其他问题或请求，我将很乐意为您提供帮助。''',
        '''我看看那''',
        '''当然，请随时浏览您需要的信息。如果您有任何问题或需要帮助，请随时告诉我。我随时待命，愿意为您服务。''',
        '''写一个js冒泡排序''',
        '''当然！这是一个使用 JavaScript 实现冒泡排序的示例代码：

```javascript
function bubbleSort(arr) {
    var len = arr.length;
    for (var i = 0; i < len - 1; i++) {
        for (var j = 0; j < len - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                var temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    return arr;
}

var numbers = [5, 3, 8, 4, 2];
console.log("排序前:", numbers);
var sortedNumbers = bubbleSort(numbers);
console.log("排序后:", sortedNumbers);
```

这段代码定义了一个 `bubbleSort` 函数，接收一个数组作为参数，并对该数组进行冒泡排序。排序后，返回排序后的数组。

在主函数中，我们定义了一个包含一些数字的数组 `numbers`。我们在控制台中打印出排序前的数组，然后使用 `bubbleSort` 函数对数组进行排序，并将排序后的结果打印到控制台中。

希望这对您有所帮助！如果有任何问题，请随时告诉我。''',
        '''当然，以下是一个使用 JavaScript 实现的冒泡排序算法：

```javascript
function bubbleSort(arr) {
  let len = arr.length;
  let swapped;
  
  do {
    swapped = false;
    for (let i = 0; i < len - 1; i++) {
      if (arr[i] > arr[i + 1]) {
        [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]]; // 交换位置
        swapped = true;
      }
    }
    len--;
  } while (swapped);
  
  return arr;
}

// 示例用法
let arr = [8, 5, 2, 9, 1, 3];
console.log("排序前:", arr);
console.log("排序后:", bubbleSort(arr));
```

上述代码定义了一个名为 `bubbleSort` 的函数，它接收一个数组作为输入，并返回已排序的新数组。代码使用了双重循环，在每一次遍历中比较相邻元素的大小，并根据需要交换它们的位置，最终将最大的元素“冒泡”到数组的末尾。循环遍历直到没有元素需要交换为止。最后，将排序后的数组返回。

以上仅是一个简单的 JS 冒泡排序算法示例，您可以根据需求进行修改和调整。希望这对您有所''',
        '''写一篇1000字文章''',
        '''抱歉，我无法一次性生成完整的1000字文章。作为一种语言模型，我的回答是根据自己的训练和编程来生成的，而且有一个输入限制。但是，如果您有特定的话题或问题，我将''',
        '''写一篇1000字文章''',
        '''在我们当前的对话中，我们共有3个上下文。第一个是关于您要求输出一篇100字诗歌的请求，第二个是关于您想要输出一篇200字的文章的请求，第三个是关于最后一次请求输出一篇200字文章的请求。希望这能帮到您，如果您还有其他问题，请随时告诉我。''',
    ]

    # 计算单条信息的token数
    single_message_tokens = [len(encoding.encode(message)) for message in dialogue]
    print("单条信息的token数:", single_message_tokens)

    # 计算多轮对话的总token数
    total_tokens = len(encoding.encode(''.join(dialogue)))
    print("多轮对话的总token数:", total_tokens)

    # 输出结果
    print(f"单条信息的token数总和: {sum(single_message_tokens)}")
    print(f"多轮对话的总token数: {total_tokens}")

    # client = openai.AzureOpenAI(
    #     api_version="2024-02-01",
    #     azure_endpoint="https://lls-gpt-japan.openai.azure.com/",
    #     api_key="e80699528657427a8d42d91cd2f6df5e",
    # )
    client = openai.OpenAI(
        base_url="http://172.16.88.207:3000/v1",
        api_key="sk-K17pLYkYVp2PJcsjBcF43181012647Ba9aC3C0A2507621B6",
    )
    try:
        tempMessage = [{
            "role": "user",
            "content": message,
        } for message in dialogue]
        chat_completion = client.chat.completions.create(
            messages=tempMessage,
            stream=False,
            model="qwen1.5-chat",
        )
        print(chat_completion.to_json())
    except Exception as err:
        print(err)


def test3():
    def get_current_weather(location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        if "tokyo" in location.lower():
            return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
        elif "san francisco" in location.lower():
            return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
        elif "paris" in location.lower():
            return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
        else:
            return json.dumps({"location": location, "temperature": "unknown"})

    # tools = [
    #     {
    #         "type": "function",
    #         "function": {
    #             "name": "get_current_weather",
    #             "description": "Get the current weather in a given location",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "location": {
    #                         "type": "string",
    #                         "description": "The city and state, e.g. San Francisco, CA",
    #                     },
    #                     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
    #                 },
    #                 "required": ["location"],
    #             },
    #         },
    #     }
    # ]

    # messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
    messages = [{'role': 'user', 'content': "What's the weather like in San Francisco?"}]
    client = openai.OpenAI(
        base_url="http://172.28.86.42:9000/v1",
        api_key="e80699528657427a8d42d91cd2f6df5e",
    )
    # client = openai.AzureOpenAI(
    #     api_version="2024-02-01",
    #     azure_endpoint="https://lls-gpt-japan.openai.azure.com/",
    #     api_key="e80699528657427a8d42d91cd2f6df5e",
    # )
    # client = openai.OpenAI(
    #     base_url="https://api.chatanywhere.tech/v1/",
    #     api_key="sk-O0qtItfZhXIjO21vcDa485ZOdtDCBohcRU1lRvKRZ4edqgSg",
    # )
    # client = openai.OpenAI(
    #     base_url="http://172.28.86.42:11434/v1/",
    #     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImFlMDE5ODk0LTJjMmQtNDMxOS05NmY3LTg4MmRmM2Y3ZmYwZCJ9.yaIXcyoNX8AhDpFq6S8JyM0P4EEHx4QskPG9ZmVzLm8",
    # )

    functions = [{
        'name': 'get_current_weather',
        'description': 'Get the current weather in a given location',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description':
                        'The city and state, e.g. San Francisco, CA',
                },
                'unit': {
                    'type': 'string',
                    'enum': ['celsius', 'fahrenheit']
                },
            },
            'required': ['location'],
        },
    }]
    response = client.chat.completions.create(
        model="Qwen1.5-7B-Chat",
        # model="lls-gpt-35",
        # model="gpt-3.5-turbo-1106",
        # model="qwen:7b",
        messages=messages,
        # tools=tools,
        functions=functions,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    print(response_message)
    return response_message


def test4():
    llm = get_chat_model({
        'model': 'Qwen1.5-7B-Chat',
        'model_server': 'http://172.28.86.42:9000/v1',
    })

    # Step 1: send the conversation and available functions to the model
    messages = [{
        'role': 'user',
        'content': "What's the weather like in San Francisco?"
    }]
    functions = [{
        'name': 'get_current_weather',
        'description': 'Get the current weather in a given location',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description':
                        'The city and state, e.g. San Francisco, CA',
                },
                'unit': {
                    'type': 'string',
                    'enum': ['celsius', 'fahrenheit']
                },
            },
            'required': ['location'],
        },
    }]

    print('# Assistant Response 1:')
    responses = []
    for responses in llm.chat(messages=messages,
                              functions=functions,
                              stream=True):
        print(responses)
    messages.extend(responses)  # extend conversation with assistant's reply

    # Step 2: check if the model wanted to call a function
    last_response = messages[-1]
    if last_response.get('function_call', None):

        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            'get_current_weather': get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = last_response['function_call']['name']
        function_to_call = available_functions[function_name]
        function_args = json.loads(last_response['function_call']['arguments'])
        function_response = function_to_call(
            location=function_args.get('location'),
            unit=function_args.get('unit'),
        )
        print('# Function Response:')
        print(function_response)

        # Step 4: send the info for each function call and function response to the model
        messages.append({
            'role': 'function',
            'name': function_name,
            'content': function_response,
        })  # extend conversation with function response

        print('# Assistant Response 2:')
        for responses in llm.chat(
                messages=messages,
                functions=functions,
                stream=True,
        ):  # get a new response from the model where it can see the function response
            print(responses)


def get_current_weather(location, unit='fahrenheit'):
    """Get the current weather in a given location"""
    if 'tokyo' in location.lower():
        return json.dumps({
            'location': 'Tokyo',
            'temperature': '10',
            'unit': 'celsius'
        })
    elif 'san francisco' in location.lower():
        return json.dumps({
            'location': 'San Francisco',
            'temperature': '72',
            'unit': 'fahrenheit'
        })
    elif 'paris' in location.lower():
        return json.dumps({
            'location': 'Paris',
            'temperature': '22',
            'unit': 'celsius'
        })
    else:
        return json.dumps({'location': location, 'temperature': 'unknown'})


def test5():
    body = '''<div>
    <includetail>
        <div style="font:Verdana normal 14px;color:#000;">
            <div style="position:relative;">
                <div class="eml-w eml-w-sys-layout">
                    <div style="font-size: 0px;">
                        <div class="eml-w-sys-line">
                            <div class="eml-w-sys-line-left"></div>
                            <div class="eml-w-sys-line-right"></div>
                        </div>
                        <div class="eml-w-sys-logo" style="float: right">
                            <img src="data:image/png;base64,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" alt=""/>
                        </div>
                    </div>
                    <div class="eml-w-sys-content">
                        <div class="dragArea gen-group-list">
                            <div class="gen-item">
                                <div class="eml-w-item-block" style="padding: 0px;">
                                    <div class="eml-w-title-level1">APIKEY通知</div>
                                </div>
                            </div>
                            <div class="gen-item" draggable="false" style="margin-top: 16px;">
                                <hr color="#E9E9E9" size="1"/>
                                <div class="eml-w-item-block" style="padding: 0px 0px 0px 1px;">
                                    <div class="eml-w-title-level3">
                                        <span>您申请的APIKEY已经创建成功。信息如下：</span>
                                        <div style="margin-top: 16px;">
                                            <table style="font-size: 14px;">
                                                <tr>
                                                    <td style="font-weight: 500">BaseURL：</td>
                                                    <td style="color: blue;">{{index . "base_url"}}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: 500">Model：</td>
                                                    <td style="color: blue;">{{index . "model"}}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: 500">APIKEY：</td>
                                                    <td style="color: blue;">sk-{{index . "token"}}</td>
                                                </tr>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="eml-w-sys-footer">BeeCloud APIKEY</div>
                </div>
            </div>
        </div><!--<![endif]-->
    </includetail>
</div>

<style>
    .eml-w-title-level1 {
        font-size: 20px;
        font-weight: 500;
        padding: 15px 0
    }

    .eml-w-title-level3 {
        font-size: 14px;
        font-weight: 500;
        padding-bottom: 10px
    }

    .eml-w-sys-layout {
        background: #fff;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, .2);
        border-radius: 4px;
        margin: 50px auto;
        max-width: 800px;
        overflow: hidden
    }

    .eml-w-sys-line-left {
        display: inline-block;
        width: 88%;
        background: #0887FF;
        height: 3px
    }

    .eml-w-sys-line-right {
        display: inline-block;
        width: 11.5%;
        height: 3px;
        background: #0887FF;
        opacity: 0.7;
        margin-left: 1px
    }

    .eml-w-sys-logo {
        text-align: right
    }

    .eml-w-sys-logo img {
        display: inline-block;
        margin: 30px 50px 0 0
    }

    .eml-w-sys-content {
        position: relative;
        padding: 20px 50px 0;
        min-height: 216px;
        word-break: break-all
    }

    .eml-w-sys-footer {
        font-weight: 500;
        font-size: 12px;
        color: #bebebe;
        letter-spacing: .5px;
        padding: 0 0 30px 50px;
        margin-top: 60px
    }

    .eml-w {
        font-family: Helvetica Neue, Arial, PingFang SC, Hiragino Sans GB, STHeiti, Microsoft YaHei, sans-serif;
        -webkit-font-smoothing: antialiased;
        color: #2b2b2b;
        font-size: 14px;
        line-height: 1.75
    }

    .eml-w a {
        text-decoration: none
    }

    .eml-w a, .eml-w a:active {
        color: #186fd5
    }

    .eml-w h1, .eml-w h2, .eml-w h3, .eml-w h4, .eml-w h5, .eml-w h6, .eml-w li, .eml-w p, .eml-w ul {
        margin: 0;
        padding: 0
    }

    .eml-w-item-block {
        margin-bottom: 10px
    }

    @media (max-width: 420px) {
        .eml-w-sys-layout {
            border-radius: none !important;
            box-shadow: none !important;
            margin: 0 !important
        }

        .eml-w-sys-layout .eml-w-sys-line {
            display: none
        }

        .eml-w-sys-layout .eml-w-sys-logo img {
            margin-right: 30px !important
        }

        .eml-w-sys-layout .eml-w-sys-content {
            padding: 0 35px !important
        }

        .eml-w-sys-layout .eml-w-sys-footer {
            padding-left: 30px !important
        }
    }
    table tr td:first-child {
        width: 100px
    }
    table {
        font-size: 16px;
    }
</style>'''
    conn = http.client.HTTPSConnection("beecloud.hrlyit.com")
    payload = json.dumps({
        "context": body,
        "name": "apikey-notify",
        "type": "email",
        "subject": "APIKEY创建成功通知",
    })
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjQwM2MyNTMwLTIxNTctNDYzOC04MzY2LTk1OTZjNDlhYmE2MCJ9.eyJpc3MiOiJodHRwczovL2JlZWNsb3VkLmhybHlpdC5jb20vdTUvYXBpL3YxIiwic3ViIjoiMWM1YzdjNjYtNGI3NS00ZTExLWI4MWMtNzliZTJlMWE4MWQ0IiwiZXhwIjoxNzE3MTkzMjY0LCJpYXQiOjE3MTcxNDI4NjQsInRlbmFudF9pZCI6IjhlZWE2NzNjLTgzYWItNDYwNS05OTlmLWRjMTE1MjE3NzIyOSIsInRlbmFudF9uYW1lIjoibGxzIiwidXNlcl9pZCI6IjFjNWM3YzY2LTRiNzUtNGUxMS1iODFjLTc5YmUyZTFhODFkNCIsInVzZXJuYW1lIjoiaGFuYm93ZW4ifQ.qD5Bu5Nh4SPWDsodITOK-qe5pE0Ck080KQ-ruG2lsSJXXIjN3QUgyQp4tmeoqHVWAQ4Ktm9oM3jq6ag74hQGnWCbxALcfy9UQi_CIKfd_KAgfcXYIS_RRCOjktWrBehCJOW9eSfx-fjhu_1wWRV7w1lFKg66jhuM2mJCiAnkztOenbHm25G_yFiPPNfvsPi86V61mWhGel70m14oGjDj-O5u0TZEEuqk5kf6RFAblySWOzhcswVkoScRlHPth4x7JSkFdH2YvAUYEeHCmY4S82TR5Fmc0gfDqPWti4BdVrnnUQbudOQxoGXdpEXJlbBaxBphgln01pkCepb3QmXc4A',
        'Content-Type': 'application/json',
    }
    conn.request("POST", "/u5/api/v1/tenants/8eea673c-83ab-4605-999f-dc1152177229/notify/template", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


test5()

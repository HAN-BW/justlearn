import os
import ast
import json
import pandas
from langchain.llms import OpenAI
import matplotlib.pyplot as plt
from langchain.globals import set_debug
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

# set_debug(True)

os.environ["OPENAI_API_KEY"] = "sk-qErp0PtswDmoGZCg8406Dc83433f4049Bd000eE6BeEb471b"
os.environ["OPENAI_API_BASE"] = "http://172.16.88.207:9997/v1"
df = pandas.read_excel("test2.xlsx", sheet_name=0)
# df2 = pandas.read_excel("test2.xlsx", sheet_name=1)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
pandas.set_option('max_colwidth', 100)
user_defined_path = os.getcwd()
user_defined_path = os.path.join(user_defined_path, "exports", "charts")
# api_key = "c4213aef4c494536846e3a401dae1ab2"
# azure_endpoint = "https://lls-gpt-japan.openai.azure.com"
# api_key = "9d31689e4ecc46508f3a4deb77cbf406"
# azure_endpoint = "https://lls-gpt-eastus.openai.azure.com/"
# api_version = "2024-02-01"

agent = create_pandas_dataframe_agent(
    # llm=AzureChatOpenAI(
    #     openai_api_key=api_key,
    #     openai_api_base=azure_endpoint,
    #     # azure_deployment="lls-gpt-35",,
    #     azure_deployment="lls-gpt-4o",
    #     openai_api_type="azure",
    #     openai_api_version=api_version,),
    llm=ChatOpenAI(temperature=0, model="qwen1.5-72b-chat", model_kwargs={"stream_options": {"include_usage": True}}),
    df=df,
    include_df_in_prompt=True,
    agent_executor_kwargs={
        "handle_parsing_errors": True,
        "save_charts_path": user_defined_path,
        "save_charts": True},
    verbose=True,
    # agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True,
    # max_iterations=5
)
response = []
# response.append(agent.invoke("分别有多少行数据"))
# response.append(agent.invoke("筛选出前三条数据"))
# response.append(agent.invoke("筛选并展示出status为OK前十条数据"))
# response.append(agent.invoke("将表1的id与表2的user_id关联获取email信息,生成表1.id,email的新表"))
# response.append(agent.invoke("通过比较表1的id与表2的user_id和表3的wecomid关联获取email信息，获取有多少条不同的email数据"))
response.append(
    agent.invoke("表的vars是一列json格式的数据，他会有多层结构，请逐层分析，提取出所有key为\"spring.datasource.username\"的值，生成一个name,env_name,key的新表"))
# response.append(
#     agent.invoke(
#         "Given a table named vars containing JSON data in a multi-level structure, the task is to extract all values corresponding to the key \"spring.datasource.username\" and generate a new table with columns named name, env_name, and key"))
# response.append(agent.invoke("你是谁"))
# response.append(agent.invoke("写一个k8s的service"))
print(str(response))

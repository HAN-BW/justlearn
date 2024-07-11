import logging
import sys
import os
import pandas
import openai
from pandasai import Agent
from pandasai import SmartDataframe
from pandasai.ee.agents.semantic_agent import SemanticAgent
from pandasai.schemas.df_config import Config
# from pandasai.llm.azure_openai import AzureOpenAI
from llama_index.llms.azure_openai import AzureOpenAI
from pandasai.responses.streamlit_response import StreamlitResponse
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from pandasai.llm.local_llm import LocalLLM
from llama_index.experimental.query_engine import PandasQueryEngine


def test1():
    df = pandas.read_excel("test.xlsx", sheet_name=0)
    api_key = "c4213aef4c494536846e3a401dae1ab2"
    azure_endpoint = "https://lls-gpt-japan.openai.azure.com"
    api_version = "2024-02-01"

    llm = AzureOpenAI(
        model="gpt-35-turbo-16k",
        deployment_name="lls-gpt-35",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )
    query_engine = PandasQueryEngine(df=df, llm=llm, verbose=True, synthesize_response=True)
    response = query_engine.query(
        "筛选出前十条task_status为successful且status为OK的数据,导出为excel",
    )
    print(str(response))


def test2():
    df = pandas.read_excel("test2.xlsx", sheet_name=0)
    api_key = "c4213aef4c494536846e3a401dae1ab2"
    llm = LocalLLM(
        model="qwen1.5-72b-chat",
        api_base="http://172.16.88.207:9997/v1",
        api_key=api_key,
    )
    user_defined_path = os.getcwd()
    user_defined_path = os.path.join(user_defined_path, "exports", "charts")
    agent = Agent(
        dfs=df,
        config=Config(
            llm=llm,
            response_parser=StreamlitResponse,
            save_charts_path=user_defined_path,
            save_charts=True,
            verbose=True
        )
    )
    # agent.add_message("筛选出前3条task_statu为successful且status为OK的数据")
    response = agent.chat(
        # "针对上述数据生成以id为横坐标，lines为纵坐标的图表",
        # "Given a table named vars containing JSON data in a multi-level structure, the task is to extract all values corresponding to the key \"spring.datasource.username\" and generate a new table with columns named name, env_name, and key",
        "表的vars是一列json格式的数据，他会有多层结构，请逐层分析，提取出所有key为\"spring.datasource.username\"的值，生成一个name,env_name,key的新表"
    )
    print(str(response))


def test3():
    # client = openai.OpenAI(
    #     base_url="http://172.16.88.207:9997/v1",
    #     api_key="sk-test"
    # )
    api_key = "c4213aef4c494536846e3a401dae1ab2"
    azure_endpoint = "https://lls-gpt-japan.openai.azure.com"
    api_version = "2024-05-01-preview"
    client = openai.AzureOpenAI(
        azure_deployment="lls-gpt-35",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )
    file = client.files.create(
        file=open("test.xlsx", "rb"),
        purpose='assistants'
    )
    # assistant = client.beta.assistants.create(
    #     instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
    #     model="lls-gpt-35",
    #     tools=[{"type": "code_interpreter"}],
    #     tool_resources={
    #         "code_interpreter": {
    #             "file_ids": [file.id]
    #         }
    #     }
    # )
    client.chat.completions.create()
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?",
                "attachments": [
                    {
                        "file_id": file.id,
                        "tools": [{"type": "code_interpreter"}]
                    }
                ]
            }
        ]
    )


test2()

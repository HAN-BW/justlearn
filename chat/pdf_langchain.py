import os
import matplotlib
import pandas
from langchain.llms import OpenAI
from langchain.globals import set_debug
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

# set_debug(True)

os.environ["OPENAI_API_KEY"] = "sk-qErp0PtswDmoGZCg8406Dc83433f4049Bd000eE6BeEb471b"
os.environ["OPENAI_API_BASE"] = "http://172.16.88.207:9997/v1"
df = pandas.read_excel("test.xlsx", sheet_name=0)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
pandas.set_option('max_colwidth', 100)
agent = create_pandas_dataframe_agent(
    llm=ChatOpenAI(temperature=0, streaming=False, model="qwen1.5-72b-chat",
                   model_kwargs={"stream_options": {"include_usage": True}}),
    df=df,
    verbose=True,
    # agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True,
    save_charts=True
)
response = []
response.append(agent.invoke("有多少行数据"))
response.append(agent.invoke("筛选出前三条数据"))
response.append(agent.invoke("筛选并展示出status为OK前十条数据"))
response.append(agent.invoke("针对前三条数据的以pending_time为纵坐标，id为横坐标生成柱状图"))
response.append(agent.invoke("针对前十条数据的以pending_time为纵坐标，id为横坐标生成柱状图"))
response.append(agent.invoke("你是谁"))
response.append(agent.invoke("写一个k8s的service"))
print(str(response))

import os
import pandas
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ["OPENAI_API_KEY"] = "sk-qErp0PtswDmoGZCg8406Dc83433f4049Bd000eE6BeEb471b"
os.environ["OPENAI_API_BASE"] = "http://172.16.88.207:9997/v1"
# os.environ["OPENAI_API_BASE"]="http://172.16.88.207:3000/v1"

if __name__ == "__main__":
    output_parser = StrOutputParser()
    df = pandas.read_excel("test2.xlsx", sheet_name=0).to_string(buf=None, columns=None, col_space=None, header=True,
                                                                 index=True, na_rep='NaN', formatters=None,
                                                                 float_format=None, sparsify=None, index_names=True,
                                                                 justify=None, max_rows=None, max_cols=None,
                                                                 show_dimensions=False, decimal='.', line_width=None,
                                                                 min_rows=None, max_colwidth=None, encoding=None)

    llm = ChatOpenAI(model="qwen1.5-72b-chat")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are world class technical documentation writer."),
        ("user", f"{df}")
    ])
    chain = prompt | llm | output_parser
    print(chain.invoke({"input": "表中的vars是一列json格式的数据，他会有多层结构，请逐层分析，提取出所有key为\"spring.datasource.username\"的值，生成一个name,env_name,key的新表"}))

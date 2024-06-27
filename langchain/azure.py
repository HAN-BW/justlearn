import requests
import json
import time
import concurrent.futures
import openai
import pandas


def azure_test(endpoint: str, api_key: str):
    df = pandas.read_excel("test.xlsx", sheet_name=0).to_string(buf=None, columns=None, col_space=None, header=True,
                                                                index=True, na_rep='NaN', formatters=None,
                                                                float_format=None, sparsify=None, index_names=True,
                                                                justify=None, max_rows=None, max_cols=None,
                                                                show_dimensions=False, decimal='.', line_width=None,
                                                                min_rows=None, max_colwidth=None, encoding=None)
    # client = openai.AzureOpenAI(
    #     api_version="2024-02-01",
    #     azure_endpoint=endpoint,
    #     api_key=api_key,
    # )
    client = openai.OpenAI(
        base_url="http://172.16.88.207:9997/v1",
        api_key=api_key,
    )
    start_time = time.time()

    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"{df}"}, {
            "role": "user",
            "content": "从中筛选出前3条task_status为successful且status为OK的数据"}],
        stream=False,
        # model="lls-gpt-4o",
        max_tokens=1500,
        model="qwen1.5-72b-chat",
    )

    chunk_time = time.time() - start_time  # calculate the time delay of the chunk
    print(f"{endpoint} Message received {chunk_time:.2f} \n {response.to_json()}\n")
    # for chunk in response:
    #     chunk_time = time.time() - start_time  # calculate the time delay of the chunk
    #     print(
    #         f"{endpoint} Message received {chunk_time:.2f} seconds after request: {chunk}\n")  # print the delay and text


tasks = [
    ("https://openai.hrlyit.com", "1af19e01a647442d95bdd6dd7dcda9e3"),
    # ("https://lls-gpt-westus3.openai.azure.com", "6fdef45fa03547898e7943631571850b"),
]

for _ in range(1):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(azure_test, url, api_key) for url, api_key in
                   tasks]
        concurrent.futures.wait(futures)

print("All tests completed.")

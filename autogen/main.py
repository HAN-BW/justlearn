import os
import datetime
import requests

from autogen import ConversableAgent, register_function


class ZeroOps:
    def __init__(self):
        self.base_url = "https://beecloud.llschain.com/zeroops/apis/v1/tenants/8b434d97-87ab-49f9-a82d-8d3c82df6d5e"
        self.headers = {
            "Authorization": f"Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhlN2Y3NjU0LWUzZGEtNGY4OS1hZTZlLTdkN2RiMjY0NzA4YiJ9.eyJpc3MiOiJodHRwczovL2JlZWNsb3VkLmxsc2NoYWluLmNvbS91NS9hcGkvdjEiLCJzdWIiOiJjYzBkMzA1OC0zM2U2LTRjZjktOWIwMi00NmIwYzJmMmY0NmIiLCJleHAiOjE3NDczMjQ5NTgsImlhdCI6MTcxNTc4ODk1OCwidGVuYW50X2lkIjoiOGI0MzRkOTctODdhYi00OWY5LWE4MmQtOGQzYzgyZGY2ZDVlIiwidGVuYW50X25hbWUiOiJsbHMiLCJ1c2VyX2lkIjoiY2MwZDMwNTgtMzNlNi00Y2Y5LTliMDItNDZiMGMyZjJmNDZiIiwidXNlcm5hbWUiOiJvcF9iZWVjbG91ZCJ9.cFWNEEg7jd_i09iUQM2YQPy5n46fek9rcxUc3ZEYzRFas6SkFidbbv6T53HyyzrWVIyC5NRRdIDYVhV3IH9C612DetoQLQg4IbGzLQiMgdj59PJn8a-hVoXuJW4TyYQJwb5qx9Acr8M2hYDvMZOBdKTzIHo85KP2wQCF99hEa6d00DOetYrVfwkI5QFWSAZ6-LG3WuyOQ498OqSIJnd-QWexi8ai-xby5SF5O8xFYelvTLWiDiX22-dfXmGL-TCNWI4dj425j_FtWBBTtQBIU_bArUM5uBphiKsYx96mrlgBmycwSQGbzNqaS3lZfZd_6GoVOMphlm97Yo65seaQ9g"
        }

    def _get(self, url, params=None):
        response = requests.get(f"{self.base_url}/{url}", headers=self.headers, params=params)
        return response.json()

    def get_top10_build(self, quantity=10):
        url = "dashboard/top_duration_builds"
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "quantity": quantity
        }
        return self._get(url, params)

    def get_build_task(self, project, service, iteration_id, tag):
        url = f"projects/{project}/services/{service}/build/tasks"
        query = {
            "iteration_id": iteration_id,
            "tag": tag
        }
        return self._get(url, query)

    def get_build_log(self, project, service, task_id):
        url = f"projects/{project}/services/{service}/build/history"
        params = {
            "task_id": task_id
        }
        return self._get(url, params)


def log_getter(num: int) -> str:
    # return "构建时间长的原因是：镜像拉取速度慢"
    z = ZeroOps()
    build = z.get_top10_build(10)["data"][num - 1]
    project = build["project_id"]
    iteration_id = build["iteration_id"]
    service = build["service_id"]
    tag = build["pipeline_run_id"]
    task = z.get_build_task(project, service, iteration_id, tag)["data"]["items"][0]
    task_id = task["id"]
    return z.get_build_log(project, service, task_id)["data"]


# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can by analyzing the build log, identify the reasons for the slow build speed. "
    "Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": [
        {
            "model": "Qwen1.5-7B-Chat",
            "base_url": "http://172.28.86.42:9000/v1",
            "api_key": "1",
        }
    ]},
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the tool signature with the assistant agent.
assistant.register_for_llm(name="log_getter", description="A build log getter")(log_getter)

# Register the tool function with the user proxy agent.
user_proxy.register_for_execution(name="log_getter")(log_getter)

register_function(
    log_getter,
    caller=assistant,  # The assistant agent can suggest calls to the log_getter.
    executor=user_proxy,  # The user proxy agent can execute the log_getter calls.
    name="log_getter",  # By default, the function name is used as the tool name.
    description="A build log getter",  # A description of the tool.
)

chat_result = user_proxy.initiate_chat(assistant, message="分析(1)构建慢的原因")

print(chat_result)

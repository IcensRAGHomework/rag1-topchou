from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

llm = AzureChatOpenAI(
    model=gpt_config['model_name'],
    deployment_name=gpt_config['deployment_name'],
    openai_api_key=gpt_config['api_key'],
    openai_api_version=gpt_config['api_version'],
    azure_endpoint=gpt_config['api_base'],
    temperature=gpt_config['temperature']
)


def generate_hw01(question):
    response = llm.invoke([
        HumanMessage(content=f"回答台灣 {question} 的紀念日有哪些，並使用 JSON 格式返回答案。")
    ])

    return response.content
def generate_hw02(question):
    pass
    
def generate_hw03(question2, question3):
    pass
    
def generate_hw04(question):
    pass
    
# def demo(question):
#     llm = AzureChatOpenAI(
#             model=gpt_config['model_name'],
#             deployment_name=gpt_config['deployment_name'],
#             openai_api_key=gpt_config['api_key'],
#             openai_api_version=gpt_config['api_version'],
#             azure_endpoint=gpt_config['api_base'],
#             temperature=gpt_config['temperature']
#     )
#     message = HumanMessage(
#             content=[
#                 {"type": "text", "text": question},
#             ]
#     )
#     response = llm.invoke([message])
#
#     return response

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder

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
examples = [{
        "input": "今年台灣10月紀念日有哪些?",
        "output": """{"Result": [{"date": "2024-10-10","name": "國慶日"}]}"""}
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You know all the holidays, and you will only return valid JSON without enclosing it in '''json'''"),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad", optional=True),
    ]
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
print(generate_hw01('2024年台灣10月紀念日有哪些?'))
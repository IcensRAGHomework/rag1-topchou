import base64

from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
import requests

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
history = {}


def get_session(session_id: str) -> BaseChatMessageHistory:
    if session_id not in history:
        history[session_id] = InMemoryChatMessageHistory()
    return history[session_id]


def get_holiday(month):
    api_url = f"https://calendarific.com/api/v2/holidays?&api_key=baa9dc110aa712sd3a9fa2a3dwb6c01d4c875950dc32vs&country=TW&year=2024&month={month}"
    response = requests.get(api_url)
    print(response.status_code)
    return response.json()


def generate_hw01(question):
    chain = final_prompt | llm
    response = chain.invoke({"input": question})

    return response.content

@tool
def generate_hw02(question):
    """
    This function answers questions about holidays in Taiwan for a specific month.
    """
    tools = [get_holiday]
    agent = create_openai_functions_agent(
        llm=llm,
        prompt=final_prompt,
        tools=tools,
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    response = agent_executor.invoke({"input": question})
    return response["output"]


def generate_hw03(question2, question3):
    pass


def load_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def generate_hw04(question):
    """
    Extracts score for a specified team from a given scoreboard image.
    Uses a structured prompt template and image input.
    """
    json_format = '{"Result":{"score": <score>} }'

    prompt_template = ChatPromptTemplate.from_messages([
        (
            'system',
            'You are a system tasked with analyzing a scoreboard. Return the result in JSON format as {json_format}.'
        ),
        (
            'human', '{input}'
        )
    ])
    # Bind the `json_format` parameter to the template
    prompt_template = prompt_template.partial(json_format=json_format)
    messages = prompt_template.format_prompt(input=question).to_messages()
    messages.append(HumanMessage([{
        'type': 'image_url',
        'image_url': {'url': f'data:image/jpeg;base64,{load_image("./baseball.png")}'}
    }]))
    response = llm.invoke(messages)
    return response.content


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
print(generate_hw04('請問中華台北的積分是多少'))

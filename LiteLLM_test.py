from llama_index.llms.litellm import LiteLLM
from llama_index.core.llms import ChatMessage
import os

# os.environ["OPENAI_API_KEY"] = "your-api-key"
# os.environ["COHERE_API_KEY"] = "your-api-key"

#  参考文档 https://docs.litellm.ai/docs/providers/openai_compatible#usage---completion


chunk_text="""
    {
        "reference": [
            "其他-人体损伤程度鉴定标准2014-01-01:    \"人体损伤程度鉴定标准2014-01-01：6.13　本标准所称的假体是指植入体内替代组织器官功能的装置，如：颅骨修补材料、人工晶体、义眼座、固定义齿（种植牙）、阴茎假体、人工关节、起搏器、支架等，但可摘式义眼、义齿等除外。\\n\",\n",
            "其他-人体损伤程度鉴定标准2014-01-01:    \"人体损伤程度鉴定标准2014-01-01：6.14　移植器官损伤参照相应条款综合鉴定。\\n\",\n",
            "其他-人体损伤程度鉴定标准2014-01-01:    \"人体损伤程度鉴定标准2014-01-01：6.15　本标准所称组织器官包括再植或者再造成活的。\\n\",\n",
            "其他-人体损伤程度鉴定标准2014-01-01:    \"人体损伤程度鉴定标准2014-01-01：6.16　组织器官缺失是指损伤当时完全离体或者仅有少量皮肤和皮下组织相连，或者因损伤经手术切除的。器官离断（包括牙齿脱落），经再植、再造手术成功的，按损伤当时情形鉴定损伤程度。\\n\",\n"
        ],
        "question": "在一次车祸中，王某的牙齿被打掉了，经过手术后医生给其植入了人工牙齿。此后，王某申请了人身损害赔偿，其律师认为王某应该被认定为组织器官缺失。请问根据《人体损伤程度鉴定标准2014-01-01》的规定，对于植入人工牙齿的情况应该如何鉴定损伤程度？",
        "answer": "根据《人体损伤程度鉴定标准2014-01-01》的规定，组织器官缺失是指损伤当时完全离体或者仅有少量皮肤和皮下组织相连，或者因损伤经手术切除的。而对于植入体内替代组织器官功能的假体，如人工牙齿，应被视为假体并非缺失的组织器官。因此，王某的情况应按损伤当时情形鉴定损伤程度。"
    },
"""
prompt="你好，牙齿被打折2颗算什么伤害?"
prompt_template = f"你是一个专业的法律大模型,请参考以下内容：{chunk_text}，以合适的语气回答用户的问题：{prompt}。如果参考内容中有图片链接也请直接返回。"

messages = [
    ChatMessage(
        role="system", content=prompt_template
    ),
    ChatMessage(role="user", content=prompt),
]

llm_deepseek = LiteLLM(
    model="openai/deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base="https://api.deepseek.com",
)
resp = llm_deepseek.chat(messages)
print(f"deepseek: {resp.message.content}")
print(f"\n")


#  参考文档
#  https://help.aliyun.com/zh/model-studio/getting-started/models?spm=a2c4g.11186623.help-menu-2400256.d_0_2.5a06b0a8FB4aX3&scm=20140722.H_2840914._.OR_help-T_cn~zh-V_1
#  https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api?spm=a2c4g.11186623.0.0.3173b0a8Pf0e94


llm_qwen = LiteLLM(
    model="openai/qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
resp = llm_qwen.chat(messages)
print(f"qwen: {resp.message.content}")
print(f"\n")

#  参考文档：
#  https://docs.litellm.ai/docs/providers/ollama

llm_ollama = LiteLLM(
    model="ollama/qwen2.5:7b",
    api_base="http://localhost:11434",
)

resp = llm_ollama.chat(messages)
print(f"ollama: {resp.message.content}")
print(f"\n")
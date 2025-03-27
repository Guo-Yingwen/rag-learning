"""
代码解释器教学示例

这个示例展示了如何使用 dashscope 的 Assistant API 创建一个具有代码执行能力的AI智能体。
整个过程分为五个主要步骤：
1. 创建智能体 (Assistant) - 配置AI智能体的功能和行为
2. 创建对话线程 (Thread) - 管理一次完整的对话会话
3. 发送消息 (Message) - 在对话线程中添加用户输入
4. 运行智能体 (Run) - 处理用户输入并生成响应
5. 处理步骤 (Steps) - 跟踪并处理智能体的执行过程
"""

import dashscope
import gradio as gr
import logging
import asyncio

# 配置日志以跟踪API调用和执行过程
logging.basicConfig(level=logging.INFO)

class CodeTeachingAssistant:
    """
    代码教学助手类
    
    工作流程：
    1. 初始化时创建助手和对话线程
    2. 接收用户消息后，将其添加到对话线程
    3. 创建运行实例处理用户输入
    4. 跟踪运行过程中的每个步骤
    5. 返回处理结果
    """
    def __init__(self):
        # 第一步：创建Assistant实例
        # - model: 选择支持代码解释器的模型
        # - tools: 启用代码解释器功能
        # - instructions: 定义Assistant的行为准则
        self.assistant = dashscope.Assistants.create(
            model='qwen-plus',  # 使用支持代码执行的千问模型
            name='编程教学助手',
            instructions='''
                你是一个编程教师，负责:
                1. 解释代码原理
                2. 提供代码示例
                3. 执行代码并分析结果
                请用通俗易懂的方式教学。
            ''',
            tools=[{'type': 'code_interpreter'}]  # 启用代码解释器
        )
        
        # 第二步：创建对话线程
        # Thread用于维护一次完整的对话上下文
        self.thread = dashscope.Threads.create()
        
    async def chat(self, message: str):
        """
        处理用户消息并返回助手回复
        
        工作流程：
        1. 将用户消息添加到对话线程
        2. 创建运行实例处理消息
        3. 跟踪运行过程中的每个步骤
        4. 逐步返回处理结果
        """
        # 第三步：发送用户消息
        # 将用户输入添加到对话线程中
        dashscope.Messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )
        
        # 第四步：创建运行实例
        # Run 负责处理用户输入并生成响应
        run = dashscope.Runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )
        
        # 用于跟踪已处理的步骤，避免重复处理
        processed_steps = set()
        
        # 第五步：处理运行步骤
        while True:
            # 获取运行状态
            run_status = dashscope.Runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
            
            # 获取执行步骤列表
            # Steps 包含了Assistant执行过程中的所有操作
            steps = dashscope.Steps.list(
                thread_id=self.thread.id,
                run_id=run.id
            )
            
            # 处理新的步骤
            if hasattr(steps, 'data'):
                for step in steps.data:
                    # 跳过已处理的步骤
                    if step.id not in processed_steps:
                        processed_steps.add(step.id)
                        
                        # 处理消息创建步骤
                        # 这类步骤包含Assistant的文本响应
                        if step.step_details.type == 'message_creation':
                            message_id = step.step_details.message_creation.message_id
                            message = dashscope.Messages.retrieve(
                                thread_id=self.thread.id,
                                message_id=message_id
                            )
                            if hasattr(message, 'content'):
                                yield message.content[0].text.value + "\n"
                        
                        # 处理代码执行步骤
                        # 这类步骤包含代码执行的过程和结果
                        elif step.step_details.type == 'tool_calls':
                            for tool_call in step.step_details.tool_calls:
                                if tool_call.type == 'code_interpreter':
                                    # 显示执行的代码
                                    yield f"\n执行代码:\n{tool_call.code_interpreter.arguments}\n"
                                    # 显示执行结果
                                    yield f"\n执行结果:\n{tool_call.code_interpreter.output}\n"
            
            # 检查运行状态
            if run_status.status == 'completed':
                break  # 处理完成
            elif run_status.status == 'failed':
                yield "处理失败，请重试"
                break  # 处理失败
                
            # 等待新的步骤
            await asyncio.sleep(1)

def create_web_ui():
    """
    创建Web交互界面
    
    使用Gradio构建简单的聊天界面，包括：
    - 对话历史显示
    - 消息输入框
    - 示例问题
    """
    assistant = CodeTeachingAssistant()
    
    css = """
        .contain { display: flex; flex-direction: column; }
        .gradio-container { height: 100vh !important; }
        #component-0 { height: 100%; }
        #chatbot { flex-grow: 1; overflow: auto;}
    """
    
    with gr.Blocks(css=css) as demo:
        chatbot = gr.Chatbot(elem_id="chatbot", label="编程学习")
        msg = gr.Textbox(label="输入问题或代码")
        
        async def respond(message, history):
            history.append((message, ""))  # 立即添加用户消息
            yield "", history  # 清空输入框并显示用户消息
            
            # 创建一个新的响应条目
            response = ""
            async for chunk in assistant.chat(message):
                response += chunk
                # 实时更新最后一条消息
                history[-1] = (message, response)
                yield "", history  # 保持输入框为空，更新对话历史
            
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        
        # 添加示例问题
        gr.Examples([
            "请用Python写一个计算斐波那契数列的函数，并画出前20个数的趋势图",
            "帮我写一个冒泡排序算法，并用随机数据测试它的效果",
            "请用matplotlib画一个简单的正弦波图形"
        ], inputs=msg)
        
    return demo

if __name__ == "__main__":
    demo = create_web_ui()
    demo.launch()
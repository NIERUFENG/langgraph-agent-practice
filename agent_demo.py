"""
LangGraph多Agent协作系统 - 精简版Demo
实现 分析->执行->审核 三Agent流水线
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
import json
from datetime import datetime


# ==================== 1. 定义状态 ====================
class AgentState(TypedDict):
    """Agent间传递的状态对象"""
    task: str                          # 原始任务
    analysis: Optional[str]            # 分析结果
    execution_plan: Optional[List[str]] # 执行计划
    execution_result: Optional[str]    # 执行结果
    review_status: Optional[str]       # 审核状态
    final_output: Optional[str]        # 最终输出
    error: Optional[str]               # 错误信息


# ==================== 2. Agent定义 ====================

def analyzer(state: AgentState) -> AgentState:
    """
    Agent 1: 分析器
    职责：理解任务，拆解为执行计划
    """
    task = state.get("task", "")
    
    # 模拟分析逻辑（真实场景会调用LLM）
    if "周报" in task:
        plan = ["收集本周工作内容", "按项目分类整理", "撰写周报正文"]
        analysis = "这是周报撰写任务，需要先收集数据再组织语言"
    elif "会议" in task:
        plan = ["提取会议讨论要点", "整理待办事项", "撰写会议纪要"]
        analysis = "这是会议纪要任务，需要提取关键决策和行动项"
    else:
        plan = ["分析任务需求", "执行任务", "输出结果"]
        analysis = f"通用任务处理：{task}"
    
    print(f"[分析Agent] 任务拆解: {plan}")
    
    return {
        **state,
        "analysis": analysis,
        "execution_plan": plan
    }


def executor(state: AgentState) -> AgentState:
    """
    Agent 2: 执行器
    职责：按计划执行具体操作
    """
    plan = state.get("execution_plan", [])
    task = state.get("task", "")
    
    # 模拟执行过程
    results = []
    for step in plan:
        # 模拟每一步执行
        results.append(f"✅ 完成: {step}")
    
    execution_result = "\n".join(results)
    print(f"[执行Agent] 执行完成:\n{execution_result}")
    
    return {
        **state,
        "execution_result": execution_result
    }


def reviewer(state: AgentState) -> AgentState:
    """
    Agent 3: 审核器
    职责：检查执行结果，决定是否通过
    """
    result = state.get("execution_result", "")
    
    # 模拟审核逻辑
    if len(result) > 20 and "完成" in result:
        status = "通过"
        final = f"【审核通过】\n任务: {state.get('task')}\n执行结果:\n{result}"
    else:
        status = "需人工复核"
        final = f"【待复核】执行结果不完整，请人工确认"
    
    print(f"[审核Agent] 审核状态: {status}")
    
    return {
        **state,
        "review_status": status,
        "final_output": final
    }


# ==================== 3. 路由决策 ====================

def should_review(state: AgentState) -> str:
    """决定执行后是否走审核"""
    # 简单逻辑：所有任务都走审核
    return "reviewer"


def should_end(state: AgentState) -> str:
    """决定审核后是否结束"""
    status = state.get("review_status", "")
    if status == "通过":
        return "end"
    else:
        # 实际可返回"executor"进行重试，这里直接结束
        return "end"


# ==================== 4. 构建Graph ====================

def build_agent_graph():
    """构建多Agent协作流程图"""
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("analyzer", analyzer)
    workflow.add_node("executor", executor)
    workflow.add_node("reviewer", reviewer)
    
    # 设置入口
    workflow.set_entry_point("analyzer")
    
    # 添加边（顺序执行）
    workflow.add_edge("analyzer", "executor")
    workflow.add_conditional_edges(
        "executor",
        should_review,
        {
            "reviewer": "reviewer"
        }
    )
    workflow.add_conditional_edges(
        "reviewer",
        should_end,
        {
            "end": END
        }
    )
    
    return workflow.compile()


# ==================== 5. 运行示例 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 多Agent协作系统启动")
    print("=" * 50)
    
    # 构建Agent图
    agent_app = build_agent_graph()
    
    # 测试任务1：周报
    print("\n📝 测试任务1: 写一份项目周报")
    result1 = agent_app.invoke({
        "task": "写一份项目周报，包含本周进度和下周计划"
    })
    print(f"\n最终输出:\n{result1.get('final_output')}")
    
    print("\n" + "-" * 30)
    
    # 测试任务2：会议纪要
    print("\n📝 测试任务2: 整理会议纪要")
    result2 = agent_app.invoke({
        "task": "整理产品需求评审会议纪要"
    })
    print(f"\n最终输出:\n{result2.get('final_output')}")
    
    print("\n" + "=" * 50)
    print("✅ 所有任务执行完毕")
    print("📌 状态流转: analyzer -> executor -> reviewer")

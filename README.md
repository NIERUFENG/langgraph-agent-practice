# LangGraph 多 Agent 协作练习

## 项目简介
基于 LangGraph 实现 Plan-Execute 模式的多 Agent 协作，练习 Agent 设计和工具调用。

## 技术栈
- LangGraph
- 自定义工具调用（@tool 装饰器）
- 链式状态传递

## 主要工作
- 设计分析 → 执行 → 发送 的 Agent 流水线
- 实现 2 个自定义工具（数据持久化 + 消息推送）
- 处理 Agent 输出的异常格式和状态传递问题

## 运行方式
pip install langgraph langchain
python agent_demo.py

## 踩坑记录
1. Agent 之间状态传递容易丢失上下文，最终通过显式 State 管理解决
2. 工具调用返回的嵌套结构解析容易出错，增加了递归取值逻辑

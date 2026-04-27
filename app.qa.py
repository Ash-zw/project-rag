from email.mime import message

import config_data as config
from rag import RagService
import streamlit as st
import time

st.title("RAG Question Answering")
st.divider()

# 初始化消息列表
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好，有什么可以帮助你的？"}]

# 初始化 RAG 服务
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# 定义 session_config（重要！）
if "session_config" not in st.session_state:
    st.session_state["session_config"] = {
        "configurable": {
            "session_id": "user_001"  # 可以根据需要动态生成
        }
    }

# 显示历史消息
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 获取用户输入
prompt = st.chat_input()

if prompt:
    # 显示用户消息
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # 显示 AI 回复的占位符
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # 流式获取响应
        with st.spinner("Loading model..."):
            res_stream = st.session_state["rag"].chain.stream(
                {"input": prompt},
                st.session_state["session_config"]
            )

            # 处理流式响应
            for chunk in res_stream:
                if chunk:  # 确保 chunk 不为空
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")  # 显示打字效果

            # 显示最终结果（去掉光标）
            message_placeholder.markdown(full_response)

    # 保存 AI 回复到历史
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
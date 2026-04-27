# 导入 streamlit 工具包，简写为 st，所有网页功能都靠它
import streamlit as st

import time

from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# 创建一个文件上传组件
uploader_file = st.file_uploader(
    "请上传TXT文件",  # 页面上显示的提示文字
    type=["txt"],  # 只允许上传 .txt 文件
    accept_multiple_files=False,  # 一次只能传一个文件
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


# 判断：如果用户真的上传了文件（不是空的）
if uploader_file is not None:
    # 从上传的文件里提取 3 个信息
    file_name = uploader_file.name  # 文件名
    file_type = uploader_file.type  # 文件类型
    file_size = uploader_file.size / 1024 # 文件大小（字节）

    # 在网页上显示二级标题：文件名
    st.subheader(f"文件名：{file_name}")

    # 在网页上显示文件信息：名字 | 类型 | 大小（转成 KB，保留2位小数）
    st.write(f"file_name: {file_name} | file_type: {file_type} | file_size: {file_size:.2f} KB")

    # 读取文件内容：
    # getvalue() 拿到二进制 bytes → decode("utf-8") 转成文字
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中......."):
        time.sleep(2)
        result = st.session_state["service"].upload_by_stream(text, file_size)
        st.write(result)
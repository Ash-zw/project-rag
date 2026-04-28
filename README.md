# 服装智能问答助手（RAG 项目）

基于 LangChain + 向量数据库的服装知识问答系统，支持尺码推荐、颜色搭配、洗涤养护等多场景服装咨询。

---

## 📋 项目功能
- 多轮对话：支持上下文记忆，理解用户的连续提问
- 知识库问答：从本地文本知识库中检索信息，给出精准回答
- 多文件支持：可导入多个 `.txt` 文档作为参考资料
- Streamlit 前端：提供简洁友好的网页交互界面

---

## 🛠️ 技术栈
- Python 3.10+
- LangChain：RAG 框架与对话链实现
- DashScopeEmbeddings / ChatTongyi：通义千问大模型接口
- Chroma：本地向量数据库
- Streamlit：Web 前端界面

---


## 📁 项目结构
```text
RAG/
├── data/                     # 📚 知识库主目录（所有参考资料放这里）
│   ├── 尺码推荐.txt          # 身高体重-尺码对照表
│   ├── 颜色推荐.txt          # 季节/肤色/场合颜色搭配指南
│   └── 洗涤养护.txt          # 面料洗护、保养知识
├── chat_history/             # 💬 对话历史存储目录（自动生成）
├── chroma_db/                # 🗄️ 向量数据库存储目录（自动生成）
├── rag.py                    # RAG 核心逻辑
├── vector_stores.py          # 向量数据库初始化与检索
├── file_history_store.py     # 对话历史持久化
├── config_data.py            # 模型与API配置
├── app.qa.py                 # Streamlit 网页入口
├── app_file_uploader.py      # 文件上传扩展功能
└── .gitignore                # Git 忽略配置

## ✅ 环境准备

### 1) 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
- 终端运行，建议虚拟环境加载，清华镜像源加速
---

## ⚙️ 配置说明

- config_data.py 中包含核心配置，根据实际需要，手动修改模型配置、chunk大小...
- 默认嵌入器 text-embedding-v4 及 Qwen3-max
- 注意，DashScope/通义千问相关的 API Key（例如 DASHSCOPE_API_KEY）需要在环境变量中先行配置
---

## 🚀 快速运行
### 1) 启动知识库上传服务
```bash
streamlit run app_file_uplodader.py
```
- 打开页面后上传 .txt 文件后，即可写入本地向量库。

### 2) 启动智能客服（RAG Chat）
```bash
streamlit run app.qa.py
```
- 输入问题后，会先检索知识库，再结合检索内容由模型综合回答
---

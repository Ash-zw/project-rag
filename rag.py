from Demos.SystemParametersInfo import new_value
from langchain_classic.tools.gmail import get_message
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from openai.resources.beta.realtime import sessions

from file_history_store import get_history
from  langchain_core.documents import Document
from vector_stores import  VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi


def print_prompt(prompt):
    print("=" * 60)
    print("📝 完整提示词：")
    print("-" * 40)

    # 打印所有消息
    for i, msg in enumerate(prompt.messages):
        print(f"\n[消息 {i}] 角色: {msg.type}")
        print("-" * 20)
        content = msg.content.replace("\\r\\n", "\n").replace("\\n", "\n")
        print(content)

    print("=" * 60)
    return prompt

class RagService(object):
    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name),
        )

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system","以我提供的参考资料为主，简洁回答提问，参考资料{context}."),
            ("system","并且我提供的用户历史记录如下"),
            MessagesPlaceholder("history"),
            ("user","请回答提问：{input}.")
        ])

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self._get_chain()


    def _get_chain(self):
        retriever=self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关资料"

            formatted_str = ""
            for doc in docs:
                # 让参考资料内容自动换行 + 格式清晰
                formatted_str += "【参考资料】\n"
                formatted_str += doc.page_content  # 直接保留原文换行
                formatted_str += "\n\n"
            return formatted_str


        def format_for_retriever(value: dict) -> str:
            return value["input"]


        def format_for_prompt_template(value) :

            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value



        chain = (
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(format_for_retriever) | retriever | format_document
            }| RunnableLambda(format_for_prompt_template) | self.prompt_template |print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain



if __name__ == "__main__":
    session_config = {
        "configurable" :{
            "session_id":"user_001"
        }
    }
    res = RagService().chain.invoke({"input":"春天穿什么颜色的衣服"},session_config)
    print(res)
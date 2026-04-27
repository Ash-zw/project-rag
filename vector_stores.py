from re import search
import config_data as config
from langchain_chroma import Chroma
from langchain_core.tools import retriever
from openai.types import embedding, vector_store


class VectorStoreService(object):

    def __init__(self,embedding):

        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory

        )


    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})



if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever=VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()

    res=retriever.invoke("体重为180斤，身高175cm,尺码推荐")
    print(res)


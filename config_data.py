

md5_path="./md5.text"


collection_name='RAG'

persist_directory='./chroma_db'
chunk_size=1000
chunk_overlap=100
separators=[
    "\n\n",    # 先按 段落分割（两个换行）
    "\n",      # 再按 单行分割
    "。",      # 再按 中文句号分割
    "！",      # 中文感叹号
    "？",      # 中文问号
    " ",       # 最后按空格
    ""         # 实在分不开就按字符切（保底）
]
max_split_char_number=100

similarity_threshold=1

embedding_model_name="text-embedding-v4"

chat_model_name="qwen3-max"

session_config = {
        "configurable" :{
            "session_id":"user_001"
        }
    }

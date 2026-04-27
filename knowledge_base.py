# 操作系统工具：判断文件是否存在、创建文件夹、读写文件
import os

# 导入项目配置文件：存放路径、切分参数、向量库配置等
import config_data as config

# Python 自带：生成 MD5 唯一标识（用于文件去重，无需安装）
import hashlib

# 向量数据库：存储文本向量
from langchain_chroma import Chroma

# 阿里通义千问嵌入模型：把文本变成向量
from langchain_community.embeddings import DashScopeEmbeddings

# 文本切分工具：把长文本切成小块
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 时间工具：给知识库添加创建时间
from datetime import datetime


# ====================== MD5 去重核心函数 ======================
def check_md5(md5_str: str):
    """检查 MD5 是否已经存在，判断文件是否重复上传"""
    # 如果保存 MD5 的文件不存在
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()  # 创建空文件
        return False  # 文件不存在 → 无重复
    else:
        # 逐行读取已保存的 MD5 并比对
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()  # 去除换行、空格
            if line == md5_str:  # 找到相同 MD5
                return True     # 文件重复
        return False            # 文件不重复


def save_md5(md5_str: str):
    """把新文件的 MD5 追加保存到文件（不会覆盖旧记录）"""
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')  # 写入并换行


def get_string_md5(input_str: str, encoding='utf-8'):
    """给文本生成唯一 MD5 身份证：内容相同 → MD5 永远相同"""
    str_bytes = input_str.encode(encoding)  # 文本转二进制
    md5_obj = hashlib.md5()                # 创建 MD5 工具
    md5_obj.update(str_bytes)              # 传入内容
    md5_hex = md5_obj.hexdigest()          # 生成 32 位 MD5
    return md5_hex


# ====================== 知识库服务核心类 ======================
class KnowledgeBaseService(object):
    def __init__(self):
        """初始化：创建向量库 + 初始化文本切分器"""
        # 创建向量库持久化目录（不存在则自动创建）
        os.makedirs(config.persist_directory, exist_ok=True)

        # 初始化 Chroma 向量库
        self.chroma = Chroma(
            collection_name=config.collection_name,    # 集合名称
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),  # 嵌入模型
            persist_directory=config.persist_directory,  # 数据保存路径
        )

        # 初始化文本切分器（把长文本切成小块）
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,        # 每块最大长度
            chunk_overlap=config.chunk_overlap,  # 块之间重叠长度
            separators=config.separators,        # 切分符号：换行、句号、空格等
            length_function=len,                 # 长度计算方式：按字符数
        )

    def upload_by_stream(self, data, filename):
        """
        上传文件到知识库
        :param data: 文件文本内容
        :param filename: 文件名
        :return: 上传结果提示
        """
        # 1. 计算文件内容的 MD5
        md5_hex = get_string_md5(data)

        # 2. 检查是否重复：重复直接返回，不入库
        if check_md5(md5_hex):
            return "内容已经存在数据库中"

        # 3. 文本切分：太长就切分，否则直接用原文
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        # 4. 元数据（给知识库内容加标签）
        metadata = {
            "source": filename,                      # 来源文件
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 上传时间
            "operator": "Ash",                       # 操作者
        }

        # 5. 把文本块批量存入向量库
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        # 6. 保存 MD5，防止下次重复上传
        save_md5(md5_hex)

        return "成功载入向量库"


# ====================== 测试代码 ======================
if __name__ == '__main__':
    service = KnowledgeBaseService()  # 初始化知识库
    r = service.upload_by_stream("Ash", "testfile")  # 测试上传
    print(r)  # 打印结果
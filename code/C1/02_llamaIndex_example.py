"""使用 LlamaIndex 构建一个最小 RAG 问答示例。

流程概览：
1. 从 .env 读取 OpenAI API Key。
2. 配置 LlamaIndex 使用的 LLM 和 Embedding 模型。
3. 读取本地 Markdown 文档。
4. 将文档构建成向量索引。
5. 基于索引创建查询引擎，并向文档提问。
"""

import os

# os.environ['HF_ENDPOINT']='https://hf-mirror.com'
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 加载 .env 文件中的环境变量，例如 OPENAI_API_KEY。
load_dotenv()

# 配置 LlamaIndex 全局使用的 LLM。
# OpenAI 类来自 llama_index.llms.openai，不是 langchain_openai。
# 如果误用 langchain_openai.OpenAI，LlamaIndex 会尝试寻找额外的 LangChain 适配包。
Settings.llm = OpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 配置 LlamaIndex 全局使用的嵌入模型。
# Embedding 模型负责把文本转换成向量，后续相似度检索依赖这些向量。
Settings.embed_model = HuggingFaceEmbedding("BAAI/bge-small-zh-v1.5")

# 读取本地 Markdown 文件，并转换成 LlamaIndex 的 Document 对象。
# input_files 使用相对于当前工作目录的路径；从项目根目录运行时可直接找到该文件。
docs = SimpleDirectoryReader(input_files=["data/C1/markdown/easy-rl-chapter1.md"]).load_data()

# 构建向量索引。
# LlamaIndex 会使用上面配置的 embed_model 为文档生成向量，并存入默认的内存向量存储。
index = VectorStoreIndex.from_documents(docs)

# 从索引创建查询引擎。
# 查询时会先检索相关文档片段，再把检索结果连同问题交给 LLM 生成答案。
query_engine = index.as_query_engine()

# 打印查询引擎内部使用的提示词模板，方便观察 LlamaIndex 如何组织上下文和问题。
print(query_engine.get_prompts())
print("=========================================================================")

# 对文档提问。答案应主要基于上面读入的 Markdown 文档内容。
print(query_engine.query("文中举了哪些例子?"))

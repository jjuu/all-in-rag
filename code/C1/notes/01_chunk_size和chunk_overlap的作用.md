`RecursiveCharacterTextSplitter()` 默认值通常是：

```python
chunk_size=4000
chunk_overlap=200
```

也就是每个文本块最多约 4000 个字符，相邻块之间重叠 200 个字符。

修改后的影响主要是这几个：

**`chunk_size` 变小**
比如改成 `500`：

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
```

结果是文本会被切得更碎。

优点：

- 检索更精确，命中的内容更聚焦
- 每次塞给 LLM 的上下文更干净
- 对问答类 RAG 通常更友好

缺点：

- 一个完整概念可能被拆散
- 文档块数量变多，向量库更大
- 检索时可能漏掉跨段落信息

**`chunk_size` 变大**
比如 `2000` 或 `4000`：

优点：

- 保留更多上下文
- 不容易把完整段落、例子、论证切碎

缺点：

- 检索结果可能不够精准
- 塞给 LLM 的无关内容更多
- 同样 `k=3` 时，会占用更多上下文窗口

**`chunk_overlap` 变大**
比如从 `200` 改成 `500`：

优点：

- 减少信息被切断的问题
- 跨 chunk 的上下文更连续

缺点：

- 重复内容变多
- 向量库变大
- 检索结果可能出现很多重复片段

**`chunk_overlap` 变小或为 0**
优点：

- chunk 数量更少
- 存储和检索更轻

缺点：

- 边界处的信息容易断开
- 问题答案刚好跨两个 chunk 时，效果会变差

对你这个中文 markdown RAG 示例，我会建议先用：

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)
```

如果你发现回答太碎、缺上下文，就把 `chunk_size` 调大到 `1000-1500`；如果发现召回内容太泛，就调小到 `500-800`。
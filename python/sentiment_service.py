# 导入需要的库
from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import json
import uvicorn

# 创建一个 FastAPI 应用
app = FastAPI(title="情感分析服务")

# 定义接收数据的格式：一条舆情包含标题、内容、来源
class News(BaseModel):
    title: str
    content: str
    source: str

# 定义接口：POST /analyze
@app.post("/analyze")
def analyze(news: News):
    # 把标题和内容拼成一段文字，交给 AI 分析
    text = f"标题：{news.title}\n内容：{news.content}"

    # 给 AI 的提示词：要求它只返回 JSON
    prompt = f"""
你是一个舆情情感分析助手。请分析下面这条舆情的情感倾向和危险等级。

{text}

请严格只返回一个 JSON，不要返回任何其他文字，格式如下：
{{
  "sentiment": "正面" 或 "负面" 或 "中性",
  "level": "高" 或 "中" 或 "低",
  "reason": "一句话说明原因"
}}

判断标准：
- 如果内容是在投诉、抱怨、骂人，sentiment 为负面，level 根据严重程度给高或中。
- 如果内容是在夸奖、表扬，sentiment 为正面，level 为低。
- 如果只是普通陈述，sentiment 为中性，level 为低。
"""

    # 调用本地 Ollama 的 qwen2.5:7b 模型
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0}  # 温度设为0，让输出更稳定
    )

    # 取出 AI 返回的文字
    raw = response["message"]["content"]

    # AI 有时候会在 JSON 前后加解释文字，我们需要提取出 JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # 如果直接解析失败，就试着从文字里找到第一个 { 和最后一个 }
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and start < end:
            data = json.loads(raw[start:end + 1])
        else:
            data = {}

    # 返回结构化结果，如果 AI 没给，就给默认值
    # 返回结构化结果，并把原始的标题、内容、来源也一并带回去
    return {
        "title": news.title,
        "content": news.content,
        "source": news.source,
        "sentiment": data.get("sentiment", "中性"),
        "level": data.get("level", "低"),
        "reason": data.get("reason", "")
    }

# 启动服务
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
# 这是一个“模拟舆情源”的接口
# 访问 http://localhost:9999/feed 会随机返回 2~4 条舆情

from fastapi import FastAPI
import random
import uvicorn

app = FastAPI(title="模拟舆情源")

# 舆情池：里面放了几条假数据
NEWS_POOL = [
    {"title": "产品被大量投诉", "content": "这款产品最近差评如潮，客服电话被打爆，用户要求退款。", "source": "weibo"},
    {"title": "新品发布会反响热烈", "content": "发布会现场掌声不断，媒体一致好评，预约量创新高。", "source": "news"},
    {"title": "服务器故障导致宕机", "content": "今天下午系统大面积宕机，用户无法登录，损失严重。", "source": "twitter"},
    {"title": "公司获得年度大奖", "content": "公司荣获行业年度最佳产品奖，团队士气高涨。", "source": "news"},
    {"title": "用户反馈物流慢", "content": "有用户吐槽发货太慢，等了五天才收到货。", "source": "forum"},
    {"title": "正常例行公告", "content": "公司发布季度例行公告，业务平稳运行。", "source": "official"},
    {"title": "紧急投诉：产品爆炸", "content": "太可怕了，产品直接爆炸了，要求巨额赔偿！", "source": "weibo"},
]

@app.get("/feed")
def feed():
    # 每次随机抽 2~4 条
    k = random.randint(2, 4)
    return random.sample(NEWS_POOL, k=min(k, len(NEWS_POOL)))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
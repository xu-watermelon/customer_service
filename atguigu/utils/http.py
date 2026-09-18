import asyncio

from httpx import AsyncClient

from atguigu.config.config import settings

# 定义变量
http_client:AsyncClient | None = None

# 初始化方法
def init_http_client():
    global http_client
    http_client = AsyncClient(timeout=10.0)

# 关闭的方法
async def close_http_client():
    if http_client is not None:
        await http_client.aclose()

# 测试调用的方法
async def test():
    init_http_client()
    response = await http_client.get(
        url="http://localhost:18081/users/u1001/orders")
    print(response.json())

if __name__ == "__main__":
    asyncio.run(test())
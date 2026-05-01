import asyncio
from deep_seek_llm import ask_llm

async def test():
    try:
        answer = await ask_llm("Say 'API works'")
        print("✅ نجح:", answer)
    except Exception as e:
        print("❌ فشل:", e)

asyncio.run(test())
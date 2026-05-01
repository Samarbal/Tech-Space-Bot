from deep_seek_llm import ask_llm_sync

try:
    res = ask_llm_sync("Say 'RAG system is ready'")
    print("✅ نجح:", res)
except Exception as e:
    print("❌ فشل:", e)
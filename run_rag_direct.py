# run_rag_direct.py - تشغيل RAG مباشرة (بدون FastAPI)
import asyncio
import json
from vector_store import search_no_metadata, add_products_no_metadata
from deep_seek_llm import ask_llm

# تحميل البيانات (تأكد من وجود data_products.json)

with open("data_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# إضافة المنتجات إلى ChromaDB (لن يعيد إضافتها إذا كانت موجودة مسبقًا)
try:
    add_products_no_metadata(products)
    print("✅ المنتجات محملة بنجاح في قاعدة المتجهات")
except Exception as e:
    print(f"⚠️ خطأ في التحميل (قد يكون مكررًا): {e}")

async def ask(question):
    # 1. البحث عن الوثائق ذات الصلة
    docs, metas = search_no_metadata(question)
    if not docs:
        return "لم أجد معلومات عن هذا المنتج في قاعدة البيانات."

    # 2. بناء الـ prompt
    context = "\n\n---\n\n".join(docs)
    prompt = f"""أنت مساعد متخصص في المنتجات التقنية. أجب على السؤال بناءً على السياق المقدم فقط.
إذا لم تكن الإجابة موجودة في السياق، قل "ليس لدي معلومات كافية".

السياق:
{context}

السؤال:
{question}

الإجابة:"""

    # 3. سؤال DeepSeek
    answer = await ask_llm(prompt)
    return answer

async def main():
    question = "Which product is the most expensive?"  # غيّر السؤال كما تحب
    print(f"\n📌 السؤال: {question}")
    answer = await ask(question)
    print(f"\n🤖 الإجابة:\n{answer}")

if __name__ == "__main__":
    asyncio.run(main())
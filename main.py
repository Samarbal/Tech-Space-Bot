# main.py  // fast api rag system 

from fastapi import FastAPI, HTTPException  # Modern, high-performance web framework
from pydantic import BaseModel  # Data validation and settings management


from vector_store import search_no_metadata, search_with_metadata
from prompt import build_rag_prompt
from deep_seek_llm import ask_llm
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # يمكن إضافة أي تهيئة عند البدء
    yield


app = FastAPI(title="Technical Product RAG Assistant", lifespan=lifespan)

class QueryRequest(BaseModel):
    question: str
    max_price: float = None
    processor: str = None
    use_metadata: bool = True
    k: int = 2

class QueryResponse(BaseModel):
    answer: str
    contexts: list
    metadata: list = None


@app.post("/ask", response_model=QueryResponse)
async def ask(req: QueryRequest):
    try:
        if req.use_metadata:
            docs, metas = search_with_metadata(
                req.question,
                max_price=req.max_price,
                processor=req.processor,
                k=req.k
            )
            metadata_out = metas
        else:
            docs = search_no_metadata(req.question, k=req.k)
            metadata_out = None
        if not docs:
            return QueryResponse(answer="No relevant products found.", contexts=[], metadata=metadata_out)
        
        
        prompt = build_rag_prompt(req.question, docs)
        
        answer = await ask_llm(prompt)

      
        return QueryResponse(answer=answer, contexts=docs, metadata=metadata_out)
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Product RAG is running. Use POST /ask"}
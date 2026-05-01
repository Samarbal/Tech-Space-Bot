#prompt.py

def build_rag_prompt(question, contexts):
    """
    contexts: list of strings (documents retrieved)
    """
    context_block = "\n\n---\n\n".join(contexts)
    prompt = f"""You are a helpful Electronic product assistant. Answer the user's question ONLY based on the context provided below.
If the answer is not present in the context, say "I don't have enough information about that."

CONTEXT:
{context_block}

QUESTION:
{question}

ANSWER (short and clear):"""
    return prompt
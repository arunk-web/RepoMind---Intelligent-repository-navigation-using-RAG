from app.retrieve import retrieve_chunks
from app.llm import get_answer_from_llm

question = "how does path generation work"

result = retrieve_chunks(question)

# Yahan tumhe context banana hai result["documents"][0] se
context = "\n\n".join(result["documents"][0])

answer = get_answer_from_llm(question, context)
print(answer)


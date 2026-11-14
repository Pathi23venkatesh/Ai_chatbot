from backend.rag import generate_answer

question = "What is the company's annual salary?"

answer = generate_answer(question)

print("Question:", question)
print("Answer:", answer)
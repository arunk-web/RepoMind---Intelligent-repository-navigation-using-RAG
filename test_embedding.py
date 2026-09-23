from app.embedding import generate_embedding

result = generate_embedding("Hello world")
print(result)
print(type(result))
print(len(result))

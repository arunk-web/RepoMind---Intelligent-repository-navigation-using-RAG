from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def hello():
    return {'message':'hello'}

# path = clone_repository("https://github.com/arunk-web/AskPDF", "storage/repos")
# print(path)

from app.repo_clone import clone_repository

path = clone_repository("https://github.com/arunk-web/AskPDF", "storage/repos")
print(path)
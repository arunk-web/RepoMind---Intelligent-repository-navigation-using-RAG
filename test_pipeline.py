from app.repo_clone import clone_repository
from app.chunk import extract_chunks_from_repo

# clone the repo
path = clone_repository("https://github.com/arunk-web/AskPDF", "storage/repos")
print("clone at: ",path)

# extract all chunnks from cloned repo
chunks = extract_chunks_from_repo(path)
print("total chunks : ", len(chunks))

for c in chunks:
    print(c["name"], "-" , c["file"])
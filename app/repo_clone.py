import git , uuid, os

def generate_unique_path(mainpath):
    unique_id = str(uuid.uuid4())
    result = os.path.join(mainpath,unique_id)
    return result


def clone_repository(url,mainpath):
    final_path = generate_unique_path(mainpath)
    git.Repo.clone_from(url,final_path)
    return final_path
import ast , os
from app.js_chunk import extract_js_chunk

def extract_chunk(file_path):
    chunks = []
    with open(file_path , 'r') as f:
        # string format
        code = f.read()
        code_lines = code.splitlines()
        # list_of_lines = list[code_lines.lineno-1:code_lines.end_lineno]

    # used to make tree
    tree = ast.parse(code)
    # print(tree)

    
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            chunk_lines = code_lines[node.lineno - 1 : node.end_lineno]
            chunk_text = "\n".join(chunk_lines)
            print(chunk_text)

            data = {
                "name" : node.name,
                "code" : chunk_text,
                "file" : file_path,
                "start_line" : node.lineno,
                "end_line" : node.end_lineno,
            }

            chunks.append(data)

        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            for method in node.body:
                if isinstance(method,ast.FunctionDef):
                    name = class_name + "." + method.name
                    chunk_lines = code_lines[method.lineno-1 : method.end_lineno]
                    chunk_text = "\n".join(chunk_lines)

                    data = {
                        "name" : name,
                        "code" : chunk_text,
                        "file" : file_path,
                        "start_line" : method.lineno,
                        "end_line" : method.end_lineno,
                    }

                    chunks.append(data)



        
            # print("got the function", node.name)
            # print("start", node.lineno)
            # print("end",node.end_lineno)
    return chunks


def extract_chunks_from_repo(repo_path):
    all_chunks = []
    for current_folder,subfolders,files in os.walk(repo_path):
        for f in files:
            final_path = os.path.join(current_folder,f)
            if f.endswith(".py"):
                required_chunk = extract_chunk(final_path)
                all_chunks.extend(required_chunk)
            elif f.endswith(".js") or f.endswith(".jsx"):
                required_chunk = extract_js_chunk(final_path)
                all_chunks.extend(required_chunk)
                
    return all_chunks



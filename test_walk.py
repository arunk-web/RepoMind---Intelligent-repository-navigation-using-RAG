import os

for current_folder,subfolders,files in os.walk("app"):
    # print("current", current_folder)
    # print("subfolder",subfolders)
    # print("files", files)
    # print("--")
    for f in files:
        if f.endswith(".py"):
            final_path = os.path.join(current_folder,f)
            print(final_path)





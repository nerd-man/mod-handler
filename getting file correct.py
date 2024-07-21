import os

def file_tree(file_path: str = ''):
    structure = {}

    for root, dirs, files in os.walk(file_path):
        item = root.replace(file_path, '').count(os.path.sep)
        # print(f'root: {item}, dirs: {dirs}, files: {files}')
        structure[os.path.basename(root)] = {
            "files": files
        }

    print(structure)


file_tree()
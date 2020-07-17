import os

def is_matrix_path_exist(path: str)->bool:
    if(os.path.exists(path)):
        return True

    return False
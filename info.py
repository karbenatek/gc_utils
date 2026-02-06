import tomllib
from gc_utils import script_dir_path

def read():
    try:
        with open(script_dir_path + '/info.toml', 'rb') as f:
            info = tomllib.load(f)
    except FileNotFoundError:
        print("❌ info.toml not found in analysis directory.")
        return None        
    return info
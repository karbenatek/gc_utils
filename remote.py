
import os
import tomllib, toml
import subprocess
import gc_utils.info as info
from gc_utils import script_dir_path, gc_utils_dir

mounts_file_path = gc_utils_dir + '/mounts.toml'
source_dictionary_path = gc_utils_dir + '/source_dictionary.toml'

# returns mounted dir paths
def get_mounts():
    try:
        with open(mounts_file_path, 'rb') as f:
            mounts = tomllib.load(f)
            return mounts
    except FileNotFoundError:
        return {'mounted_paths': []}
        
# add new mount path to mounts.toml      
def log_mount(mount_path):
    mounts = get_mounts()

    if mounts is None:
        mounts = {'mounted_paths': [mount_path]}
    elif mount_path not in mounts.get('mounted_paths'):
        mounts['mounted_paths'].append(mount_path)
    # update mounts.toml
    with open(mounts_file_path, 'wb') as f:
        f.write(toml.dumps(mounts).encode('utf-8'))
    
def get_source_dictionary():
    with open(source_dictionary_path, 'rb') as f:
        source_dict = tomllib.load(f)['source_dictionary']
    
    return source_dict
            
# get local analysis info from info.toml
# def read_info():
#     try:
#         with open(script_dir_path + '/info.toml', 'rb') as f:
#             info = tomllib.load(f)
#     except FileNotFoundError:
#         print("❌ info.toml not found in analysis directory.")
#         return None        
#     return info

# check if data is mounted in data directory
def data_mounted():
    in_here = os.listdir(script_dir_path)
    return 'data' in in_here

# mount data directory using rclone 
def mount_data():
    # print(f"Script path: {script_dir_path}")
    
    analysis_info = info.read()
    if analysis_info.get('data') is None:
        return

    if not analysis_info:
        print(f"❌ No analysis info here - nothing mounted.\n By here I mean {script_dir_path}")
        return
    
    mount_path = script_dir_path + '/mount'
    
    mounted_paths = get_mounts().get('mounted_paths')
    print(f"Mounted paths: {mounted_paths}")
    
    if not mounted_paths or mount_path not in mounted_paths:
        os.makedirs(mount_path, exist_ok=True)
    else:
        return
    
    source_dictionary = get_source_dictionary()  
    data_source_path =  source_dictionary[analysis_info['data']['source']] + '/' + analysis_info['data']['path']
    
    
    cmd = [
        'rclone',
        'mount',
        data_source_path, 
        mount_path, 
        "--vfs-cache-mode", "writes",'--daemon']
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Mounted {data_source_path} to ./data")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to mount: {e}")
        
    ## add absolute path to file mounts.toml
    log_mount(mount_path)
    
    

    # if 'GC_MOUNTS' in os.environ:
    #     os.environ['GC_MOUNTS'] += data_path + os.pathsep
    # else:
    #     os.environ['GC_MOUNTS'] = data_path + os.pathsep
        
def umount():
    mount_paths = get_mounts().get('mounted_paths')
    if mount_paths is None:
        print("No mounted paths found.")
        return
    
    for path in mount_paths:
        cmd = ['fusermount', '-u', path]
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Unmounted {path}")
            # delete empty mount dir
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to unmount {path}: {e}")
            
        os.removedirs(path)
    # remove mounts.toml file
    os.remove(mounts_file_path)
        
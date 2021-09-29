import hashlib
import psutil
import csv
import os
import glob

def initialize():
    paths = []
    services = list(psutil.process_iter())
    for item in services:
        try:
            path = psutil.Process(item.pid).exe()
            if path not in paths:
                paths.append(path)
        except Exception as e:
            print(e)
    update_paths(paths)
    get_parents(paths)

def get_parents(paths):
    parent_dirs = []
    for path in paths:
        parent_path = os.path.dirname(path)
        if parent_path not in parent_dirs:
            parent_dirs.append(parent_path)
    get_dlls(parent_dirs)

def get_dlls(paths):
    dll_list = []
    for path in paths:
        dlls = glob.glob(path + "\\*.dll")
        for dll in dlls:
            dll_list.append(dll)
    update_paths(dll_list)

def update_paths(paths):
    with open("paths.txt", 'a') as f:
        for path in paths:
            f.write(path + "\n")

def get_hash(path):
    try:
        with open(path, 'rb') as f:
            exe_hash = hashlib.md5()
            while chunk := f.read(8192):
                exe_hash.update(chunk)
            return exe_hash
    except Exception as e:
        print(e)
        return None

def get_all_hashes():
    paths = []
    with open("paths.txt", "r") as f:
        for path in f:
            paths.append(path.strip())
    
    hash_dict = {}
    for path in paths:
        path = path.replace('"', "")
        try:
            file_hash = get_hash(path)
            hash_dict.update({path: file_hash.hexdigest()})
        except:
            continue

    print_dict_csv(hash_dict)

def print_dict_csv(dic):
    with open("hashes.csv", "w") as f:
        for key in dic.keys():
            f.write("%s,%s\n"%(key, dic[key]))

def compare_hashes(file):
    with open(file) as f:
        csvd = csv.reader(f)
        for line in csvd:
            new_hash = get_hash(line[0])
            if new_hash.hexdigest() != line[1]:
                print(line[0] + " hash has changed")
        
def main():
    initialize()
    get_all_hashes()

if __name__ == "__main__":    
    main()

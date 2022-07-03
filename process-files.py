import os
import sys

def bytes_as_str(num_bytes: int) -> str:
    gbs = num_bytes / 2**(30)
    if gbs >= 1:
        return f"{gbs:4.2f} GB"
    mbs = gbs * 1024
    if mbs >= 1:
        return f"{mbs:4.2f} MB"
    kbs = mbs * 1024
    if kbs >= 1:
        return f"{kbs:4.2f} MB"
    bb = kbs * 1024
    if bb >= 1:
        return f"{bb:4.2f} bytes"

def process_files(root_dir: str) -> int:
    # get all files inside a specific folder
    with os.scandir(path=root_dir) as root:
        dir_size = 0
        for entry in root:
            if entry.is_dir():
                dir_size += process_files(entry.path)
            elif entry.is_file():
                stat = os.stat(entry.path)
                dir_size += stat.st_size
        print(f"Files and Directories in {root_dir} {bytes_as_str(dir_size)}")
        return dir_size

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: python process-files.py <root_dir>")
        pass
    elif len(sys.argv) > 1:
        root_dir = sys.argv[1]
        process_files(root_dir)
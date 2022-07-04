import os
import sys
from typing import List
from file_info import FileInfo

def get_bytes_as_str(total_bytes: int) -> str:
    gbs = total_bytes / 2**(30)
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

def get_file_info(path: str) -> FileInfo:
    stat = os.stat(path)
    return FileInfo(path=path, bytes=stat.st_size)

def get_file_infos_total_bytes(file_infos: List[FileInfo]) -> int:
    total_bytes = 0
    for file_info in file_infos:
        total_bytes += file_info.bytes
    return total_bytes

def process_files(root_dir: str) -> List[FileInfo]:
    # get all files inside a specific folder
    with os.scandir(path=root_dir) as root:
        dir_size = 0
        file_infos = []
        for entry in root:
            if entry.is_dir():
                file_infos.extend(process_files(entry.path))
            elif entry.is_file():
                file_infos.append(get_file_info(entry.path))
        size = get_bytes_as_str(get_file_infos_total_bytes(file_infos))
        print(f"Files and Directories in {root_dir} {size}")
        return file_infos

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: python process-files.py <root_dir>")
        pass
    elif len(sys.argv) > 1:
        root_dir = sys.argv[1]
        process_files(root_dir)
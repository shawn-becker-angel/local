import sys
from file_info import FileInfo

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: python process-files.py <root_dir>")
        pass
    elif len(sys.argv) > 1:
        file_info = FileInfo(parent=None, path=sys.argv[1])
        total_bytes = file_info.get_bytes()
        for child in file_info.children:
            print(child)

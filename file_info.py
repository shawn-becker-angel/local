# file: file-info.py_compile

import os

# get_bytes is always computed
class FileInfo:
    
    parent = None
    path = None
    level = 0
    children = None
    
    def __init__(self,parent,path,level=0):
        self.parent = parent
        self.path = path
        self.level = level
        if os.path.isdir(path):
            with os.scandir(path) as dir:
                self.children = []
                for entry in dir:
                    child = FileInfo(parent=self, path=entry.path, level=level+1)
                    self.children.append(child)
                # print(f"{' ' * self.level} D {self.path} num_files:{len(self.children)}")
        else:
            # print(f"{' ' * self.level} {self.path}")
            pass

    def get_bytes_as_str(self, total_bytes: int) -> str:
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

    def print(self) -> int:
        total_bytes = 0
        path = self.path
        level = self.level
        file_type = ''
        if os.path.isfile(path):
            total_bytes += os.stat(self.path).st_size
        elif os.path.isdir(path):
            file_type = 'D'
            for child in self.children:
                child_path = child.path # for debugging
                total_bytes += child.print()
            print(f"{' ' * self.level} {file_type} {self.path} {len(self.children)} files {self.get_bytes_as_str(total_bytes)}")
        return total_bytes

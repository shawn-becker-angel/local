# file: file-info.py_compile

import os
import functools
from functools import total_ordering


# get_bytes is always computed

@total_ordering
class FileInfo:
    
    parent = None
    path = None
    level = 0
    children = None
    bytes = 0
    is_dir = False
    
    def __init__(self,parent,path,level=0):
        self.parent = parent
        self.path = path
        self.level = level
        if os.path.isdir(path):
            self.is_dir = True
            with os.scandir(path) as dir:
                self.children = []
                for entry in dir:
                    child = FileInfo(parent=self, path=entry.path, level=level+1)
                    self.children.append(child)
                # print(f"{' ' * self.level} D {self.path} num_files:{len(self.children)}")
        else:
            self.isDir = False
            # print(f"{' ' * self.level} {self.path}")

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

    # compute file and directory sizes in bytes recursively
    # sort all files in each directory by bytes descending
    # return the total bytes of the file or directory
    def get_bytes(self) -> int:
        total_bytes = 0
        if os.path.isfile(self.path):
            self.bytes = os.stat(self.path).st_size
            total_bytes += self.bytes
        elif os.path.isdir(self.path):
            for child in self.children:
                child_path = child.path # for debugging
                total_bytes += child.get_bytes()
            self.bytes = total_bytes
            self.children = sorted(self.children, reverse=True)
        return total_bytes
    
    
    # required for @total_ordering
    def __lt__(self, obj):
        return ((self.bytes) < (obj.bytes))
  
    def __gt__(self, obj):
        return ((self.bytes) > (obj.bytes))
  
    def __le__(self, obj):
        return ((self.bytes) <= (obj.bytes))
  
    def __ge__(self, obj):
        return ((self.bytes) >= (obj.bytes))
  
    def __eq__(self, obj):
        return (self.bytes == obj.bytes)
  
    def __repr__(self):
        prefix = 'Dir' if self.is_dir else 'File'
        return f'{prefix}("{os.path.basename(self.path)}","{self.get_bytes_as_str(self.bytes)})'

    def __str__(self):
        if self.is_dir:
            return f"{'   ' * self.level} D {os.path.basename(self.path)} bytes:{self.bytes} files:{len(self.children)} max:{self.children[0].bytes} min:{self.children[-1].bytes}"
        else:
            return ''


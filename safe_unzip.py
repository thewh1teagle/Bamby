import os, io, re
import resource
import contextlib
from typing import Type
from zipfile import ZipFile


@contextlib.contextmanager
def limit(ram_limit, disk_limit):
    ram_resource = resource.RLIMIT_FSIZE
    disk_resource = resource.RLIMIT_AS
    soft_disk_limit, hard_disk_limit = resource.getrlimit(ram_resource)
    soft_ram_limit, hard_ram_limit = resource.getrlimit(disk_resource)
    
    resource.setrlimit(ram_resource, (ram_limit, hard_ram_limit))
    resource.setrlimit(disk_resource, (disk_limit, hard_disk_limit))
    try:
        yield
    finally:
        resource.setrlimit(ram_resource, (soft_ram_limit, hard_ram_limit))
        resource.setrlimit(disk_resource, (soft_disk_limit, hard_disk_limit))
    

def unzip(path='', path_from_local=''):
    filepath = path_from_local + path
    extract_path = filepath.strip('.zip') + '/'

    parent_archive = ZipFile(filepath)
    parent_archive.extractall(extract_path)
    namelist = parent_archive.namelist()
    
    parent_archive.close()
    for name in namelist:
        try:
            if name.endswith('.zip'):
                unzip(path=name, path_from_local=extract_path)
        except (OSError, MemoryError, TypeError):
            raise
        except Exception as e:
            print('Failed on ', name)
            pass
    return extract_path


if __name__ == '__main__':
    RAM_LIMIT = int( (1024*1024*1024) * 0.5 ) # 0.5GB
    DISK_LIMIT = (1024*1024*1024) * 1 # 1GB
    with limit(RAM_LIMIT, DISK_LIMIT):
        unzip('bomb.zip')
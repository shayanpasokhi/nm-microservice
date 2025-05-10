import hashlib

def compute_file_hash(path, method='sha256'):
    if method == 'md5':
        h = hashlib.md5()
    elif method == 'sha256':
        h = hashlib.sha256()
    elif method == 'sha512':
        h = hashlib.sha512()
    else:
        raise ValueError("Unsupported hash method")

    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

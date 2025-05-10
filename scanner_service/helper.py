import os

def get_unique_path(dest_dir, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    full_path = os.path.join(dest_dir, new_filename)
    while os.path.exists(full_path):
        new_filename = f"{name}({counter}){ext}"
        full_path = os.path.join(dest_dir, new_filename)
        counter += 1
    return full_path

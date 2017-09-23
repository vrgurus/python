import os


def remove_zero_byte_file(search_path):
    target_size = 0
    for dirpath, dirs, files in os.walk(search_path):
        for file in files: 
            path = os.path.join(dirpath, file)
            print('%s:%s' % (path,os.stat(path).st_size))
            if os.stat(path).st_size == target_size:
                os.remove(path)



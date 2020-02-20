''''''

import os
import zipfile
from random import shuffle


def random_string(length=8):
    ''''''
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s_length = 62
    while length > s_length:
        s += s
        s_length += 62
    s_list = list(s)
    shuffle(s_list)
    return ''.join(s_list[:length])

def zip_dir(in_file_dir, out_file_path):
    ''''''
    f = zipfile.ZipFile(out_file_path, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(in_file_dir):
        fpath = dirpath.replace(in_file_dir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            f.write(os.path.join(dirpath, filename), fpath+filename)
    f.close()

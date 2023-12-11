import os
import glob

from read_data import Read_data

name = 'pkgs'

if os.path.exists(name):
    print(f'folder {name} already exists')
else:
    os.mkdir(name)

# download .tar files from RnDNet to pkgs folder

obj = Read_data()

# get .tar files
files = list(map(lambda x: os.path.basename(x), glob.glob(name + '/*.tar')))

for f_name in files:

    pkg_num = f_name.split('.')[0]

    path_to_pkg = name + f'/{pkg_num}'
    path_to_tar_file = name + f'/{f_name}'

    if os.path.exists(path_to_pkg):
        print(f'folder {pkg_num} already exists')
    else:
        obj.path_to_file = path_to_tar_file
        obj.path_to_extract = path_to_pkg
        obj.read_tar_file()

    obj.path_to_file = path_to_pkg + '/' + os.listdir(path_to_pkg)[0]
    meta = obj.read_meta()
    label = obj.read_label()

    print(f'package {pkg_num} files, ', os.listdir(obj.path_to_file + '/files'))

pass

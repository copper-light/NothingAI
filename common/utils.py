import os
import shutil
import logging
import datetime
from distutils.dir_util import copy_tree

from django.core.files.storage import FileSystemStorage
from config import settings

logger = logging.getLogger('common.utils')


def get_files(path, sub_directory=None, root_directory=settings.FILE_UPLOAD_DIR):
    if path.startswith('/'):
        path = path[1:]

    if sub_directory is not None:
        if sub_directory.startswith('/'):
            sub_directory = sub_directory[1:]
        base_dir = os.path.join(root_directory, str(sub_directory))
    else:
        base_dir = root_directory

    real_path = os.path.join(base_dir, str(path))
    if not os.path.exists(real_path):
        return None

    created = datetime.datetime.fromtimestamp(os.path.getmtime(real_path))
    updated = datetime.datetime.fromtimestamp(os.path.getatime(real_path))

    if os.path.isfile(real_path):
        ret = [
            {
                'name': os.path.split(path)[1], 'type': 'file',
                'created_at': created, 'updated_at': updated, 'size': os.path.getsize(real_path)}
        ]
    else:
        files = os.listdir(real_path)
        ret = []
        for file in files:
            full_path = os.path.join(real_path, file)

            if os.path.isfile(full_path):
                ret.append({
                    'name': file,
                    'type': 'file',
                    'created': created, 'updated_at': updated, 'size': os.path.getsize(full_path)})
            else:
                ret.append({
                    'name': file,
                    'type': 'dir',
                    'created': created, 'updated_at': updated, 'size': ''})

    return ret


def save_files(request_files, root_directory=settings.FILE_UPLOAD_DIR, sub_directory=None, overwrite=True):
    ret = True
    is_overwritten = False
    file_fields = list(request_files.keys())
    if sub_directory is not None:
        base_dir = os.path.join(root_directory, str(sub_directory))
    else:
        base_dir = root_directory

    fs = FileSystemStorage()
    for sub_dir in file_fields:
        files = request_files.getlist(sub_dir)
        if sub_dir.startswith('/'):
            sub_dir = sub_dir[1:]
        save_dir = os.path.join(base_dir, sub_dir)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for f in files:
            save_file_path = os.path.join(str(save_dir), f.name)

            if os.path.exists(save_file_path):
                if overwrite:
                    is_overwritten = True
                    os.remove(save_file_path)
                else:
                    raise FileExistsError(os.path.join('/', str(sub_dir), f.name))

            fs.save(save_file_path, f.file)
            if is_overwritten:
                logger.debug('Overwritten the file: {}'.format(save_file_path))
            else:
                logger.debug('Created the file: {}'.format(save_file_path))

    return ret


def rm_files(path, root_directory=settings.FILE_UPLOAD_DIR, sub_directory=None, force=False):
    if path.startswith('/'):
        path = path[1:]

    if sub_directory is not None:
        if sub_directory.startswith('/'):
            sub_directory = sub_directory[1:]
        base_dir = os.path.join(root_directory, str(sub_directory))
    else:
        base_dir = root_directory

    real_path = os.path.join(base_dir, str(path))
    if not os.path.exists(real_path):
        raise FileNotFoundError(os.path.join('/', path))

    if os.path.isfile(real_path):
        os.remove(real_path)
    else:
        if force:
            shutil.rmtree(real_path)
        else:
            os.rmdir(real_path)

    return True


def copy_files(src_path, dst_path, overwrite=False):
    if not os.path.exists(src_path):
        raise FileNotFoundError(src_path)

    if overwrite:
        copy_tree(src_path, dst_path)
    else:
        shutil.copytree(src_path, dst_path)

    return True


if __name__ == '__main__':
    d = os.path.join(settings.EXPERIMENTS_DIR, '1')
    s = '/Users/handh/dev/python/NotingAI/upload_files/models/1'

    copy_files(s, d, overwrite=True)
    rm_files(d, root_directory='/', force=True)


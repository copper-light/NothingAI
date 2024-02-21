import os
import shutil
import logging

from django.core.files.storage import FileSystemStorage
from django.conf import settings

logger = logging.getLogger('common.utils')


def save_files(request_files, root_directory=settings.FILE_UPLOAD_DIR, sub_directory=None, clear_dir=False, overwrite=True):
    ret = True
    file_fields = list(request_files.keys())
    is_backed_up = False
    if sub_directory is not None:
        base_dir = os.path.join(root_directory, str(sub_directory))
    else:
        base_dir = root_directory

    try:
        if os.path.exists(base_dir):
            if clear_dir:
                shutil.move(base_dir, '{}_bak'.format(base_dir))
                is_backed_up = True
        else:
            os.makedirs(base_dir)

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
                if overwrite and os.path.exists(save_file_path):
                    os.remove(save_file_path)
                fs.save(save_file_path, f.file)
                logger.debug('Save the file: {}'.format(save_file_path))
    except FileExistsError as e:
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        logger.error(e)
        ret = False

    finally:
        if is_backed_up:
            if ret:
                shutil.rmtree('{}_bak'.format(base_dir))
            else:
                shutil.move('{}_bak'.format(base_dir), base_dir)

    return ret

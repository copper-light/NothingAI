import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def save_files(request_files, root_directory=settings.FILE_UPLOAD_DIR, sub_directory=None, clear_dir=True, overwrite=True):
    file_fields = list(request_files.keys())

    if sub_directory is not None:
        base_dir = os.path.join(root_directory, str(sub_directory))
    else:
        base_dir = root_directory

    try:
        if os.path.exists(base_dir):
            if clear_dir:
                os.removedirs(base_dir)
            else:
                os.makedirs(base_dir)
        else:
            os.makedirs(base_dir)
    except FileExistsError as e:
        return False

    fs = FileSystemStorage()
    for sub_dir in file_fields:
        files = request_files.getlist(sub_dir)
        if sub_dir.startswith('/'):
            save_dir = os.path.join(base_dir, sub_dir[1:])
        else:
            save_dir = base_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        print(files)
        for f in files:
            save_file_path = os.path.join(save_dir, f.name)
            if overwrite and os.path.exists(save_file_path):
                os.remove(save_file_path)
            fs.save(save_file_path, f.file)
            print('save {}'.format(f.name))

    ## 트라이캐치로 실패했을때 폴더들 삭제하는 문구 추가

    return False

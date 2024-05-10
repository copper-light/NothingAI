import os
import glob
import shutil
import logging
import datetime
from distutils.dir_util import copy_tree

import tailer
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


class TaskLogger:

    def __init__(self, log_dir, log_filename=settings.TASKS_LOG_FILENAME, log_limit=settings.TASK_LOG_SIZE, clear_logs=False):
        self.line_number = 0
        self.log_dir = log_dir
        self.log_filename = log_filename
        self.log_limit = log_limit
        self.file = None
        self.file_no = 0

        if clear_logs and os.path.exists(self.log_dir):
            rm_files(self.log_dir, root_directory='/', force=True)

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self._check()

    def _get_last_line_number(self):
        log_files = glob.glob(os.path.join(self.log_dir, self.log_filename.format('*')))
        line_number = None
        if len(log_files) > 0:
            filename = log_files[-1]
            output = tailer.tail(open(filename, 'r'), lines=1)
            if output is not None:
                token = output[0].split(':')
                if len(token) > 0:
                    line_number = token[0]
                    try:
                        line_number = int(line_number)
                    except ValueError:
                        line_number = None
        return line_number

    def _check(self):
        self.line_number = self._get_last_line_number() or 0
        self.file_no = self.line_number // self.log_limit * self.log_limit
        self._open()

    def _open(self):
        if self.file is not None:
            self.file.close()
        self.file = open(os.path.join(self.log_dir, self.log_filename.format(self.file_no)), 'a')

    def write(self, message, auto_flush=True):
        self.line_number += 1
        self.file.write(f'{self.line_number}:{message.strip()}\n')
        if auto_flush:
            self.file.flush()

        after_no = self.line_number // self.log_limit * self.log_limit
        if self.file_no != after_no:
            self.file_no = after_no
            self._open()

    def read(self, offset, limit):
        task_output_log = os.path.join(self.log_dir, self.log_filename)
        log_files = glob.glob(os.path.join(self.log_dir, self.log_filename.format('*')))

        if limit is None or int(limit) > 100:
            limit = 100
        else:
            limit = int(limit)

        if offset is None:
            if len(log_files) >= 2:
                file_no1 = (len(log_files) - 2) * settings.TASK_LOG_SIZE
                file_no2 = (len(log_files) - 1) * settings.TASK_LOG_SIZE
            else:
                file_no1 = None
                file_no2 = (len(log_files) - 1) * settings.TASK_LOG_SIZE

            outputs = tailer.tail(open(task_output_log.format(file_no2)), lines=limit)
            remaining_line = limit - len(outputs)

            if remaining_line > 0 and file_no1:
                front_output = tailer.tail(open(task_output_log.format(file_no1)), lines=remaining_line)
                front_output.extend(outputs)
                outputs = front_output
        else:
            offset = int(offset)
            if offset == 0:
                offset = 1
            file_no1 = offset // settings.TASK_LOG_SIZE * settings.TASK_LOG_SIZE
            file_no2 = (offset + limit - 1) // settings.TASK_LOG_SIZE * settings.TASK_LOG_SIZE

            if file_no1 == file_no2:
                file_no2 = None

            outputs = []
            last_line = tailer.tail(open(task_output_log.format(file_no1)), lines=1)
            if len(last_line) > 0:
                line_number, msg = last_line[0].split(':')
                if line_number:
                    read_line_count = int(line_number) - offset + 1
                    if read_line_count > 0:
                        outputs = tailer.tail(open(task_output_log.format(file_no1)), lines=read_line_count)

            remaining_line = limit - len(outputs)

            if remaining_line > 0 and file_no2:
                post_output = tailer.head(open(task_output_log.format(file_no2)), lines=remaining_line)
                outputs.extend(post_output)
            else:
                if remaining_line < 0:
                    outputs = outputs[:remaining_line]

        if len(outputs) > 0:
            line_number, msg = outputs[0].split(':')
            if line_number:
                offset = int(line_number)
            else:
                offset = None
        else:
            offset = 0

        limit = len(outputs)

        if limit == 0:
            next_offset = 0
        else:
            next_offset = offset + limit

        return outputs, offset, limit, next_offset


# def rotate_log(file_path, append=False):
#     if append:
#         output = tailer.tail(file_path, lines=1)
#     else:
#         output = tailer


if __name__ == '__main__':
    d = os.path.join(settings.EXPERIMENTS_DIR, '1')
    s = '/Users/handh/dev/python/NotingAI/upload_files/models/1'

    copy_files(s, d, overwrite=True)
    rm_files(d, root_directory='/', force=True)


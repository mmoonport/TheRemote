import traceback
import os
import re
import logging as log

def sp(path, *args):

    # Standardise encoding, normalise case, path and strip trailing '/' or '\'
    if not path or len(path) == 0:
        return path

    # convert windows path (from remote box) to *nix path
    if os.path.sep == '/' and '\\' in path:
        path = '/' + path.replace(':', '').replace('\\', '/')

    path = os.path.normpath(ss(path, *args))

    # Remove any trailing path separators
    if path != os.path.sep:
        path = path.rstrip(os.path.sep)

    # Add a trailing separator in case it is a root folder on windows (crashes guessit)
    if len(path) == 2 and path[1] == ':':
        path = path + os.path.sep

    # Replace *NIX ambiguous '//' at the beginning of a path with '/' (crashes guessit)
    path = re.sub('^//', '/', path)

    return path

def remove_pyc(folder, only_excess = True, show_logs = True):

    folder = sp(folder)

    for root, dirs, files in os.walk(folder):

        pyc_files = filter(lambda filename: filename.endswith('.pyc'), files)
        py_files = set(filter(lambda filename: filename.endswith('.py'), files))
        excess_pyc_files = filter(lambda pyc_filename: pyc_filename[:-1] not in py_files, pyc_files) if only_excess else pyc_files

        for excess_pyc_file in excess_pyc_files:
            full_path = os.path.join(root, excess_pyc_file)
            if show_logs: log.debug('Removing old PYC file: %s', full_path)
            try:
                os.remove(full_path)
            except:
                log.error('Couldn\'t remove %s: %s', (full_path, traceback.format_exc()))

        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            if len(os.listdir(full_path)) == 0:
                try:
                    os.rmdir(full_path)
                except:
                    log.error('Couldn\'t remove empty directory %s: %s', (full_path, traceback.format_exc()))

def get_data_dir():
    pass
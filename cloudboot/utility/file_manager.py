import hashlib
import os
import shutil
from os.path import isfile, isdir
from zipfile import ZipFile


def path_exists(path):
    """Check whether the given directory exists.

    Parameters
    ------------------
    path: str
        Path to the directory.
    """
    return isdir(path)


def file_exists(path):
    """Check whether the given file exists.

    Parameters
    ------------------
    path: str
        Path to the file.
    """
    return isfile(path)


def write_data(content, path):
    """Creates file objects.

    Writes given data object into a file as binary data. Used in downloading templates from a remote URL.

    Parameters
    ---------------------
    content: any
        Data object to be saved.
    path: str
        Path to the file which data object need to be saved.
    """
    with open(path, 'wb') as file_obj:
        return file_obj.write(content)


def extract_zip_file(source, target, src_dir=None):
    """Extracts zip archive.

    Extracts given .zip archive file into a target location and modify the source files root for the given context.
    Archive file won't get deleted after the extraction.

    Parameters
    -------------------------------
    source: str
        Path to .zip file.
    target: str
        Path where zip file needs to be extracted into.
    src_dir: str
        Actual directory which contains sources of the extracted archive.

    """
    create_directory(target)
    with ZipFile(source) as archive:
        archive.extractall(target)
    if src_dir:
        src_dir = f'{target}/{src_dir}'
        os.system(f'mv {src_dir}/* {target}/')
        shutil.rmtree(src_dir)


def create_directory(path):
    os.makedirs(path)


def calculate_checksum(path):
    """Calculates the checksum of a file.

    Parameters
    ----------------------
      path: str
        The path to the source file.
    """
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def directory_checksum(path):
    """Retrieve checksum of a source directory

    Calculates and concatenate checksums of a given directory tree.

    Parameters
    -----------------------
    path: str
        Path to the source directory.
    """
    checksum = ""
    for root, dirs, files in os.walk(path):
        for filename in files:
            file_checksum = calculate_checksum(os.path.join(root, filename))
            checksum += file_checksum
    return checksum

from cloudboot.config import SRC_DIR
from cloudboot.utility.downloader import download_template
from cloudboot.utility.file_manager import extract_zip_file


def create_function(name, runtime, trigger, options=None):
    archive = download_template(runtime, trigger)
    extract_zip_file(archive, '/'.join([SRC_DIR, name]))

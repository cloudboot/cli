ROOT_DIR = '/home/lpsandaruwan/Desktop/cloudboot/temp'
SRC_DIR = '/'.join([ROOT_DIR, 'src'])
CACHE_DIR = '/'.join([ROOT_DIR, '.cloudboot'])


def reset_root(path='.'):
    global ROOT_DIR, SRC_DIR, CACHE_DIR
    ROOT_DIR = path
    SRC_DIR = '/'.join([ROOT_DIR, '.cloudboot'])
    CACHE_DIR = '/'.join([ROOT_DIR, '.cloudboot'])
